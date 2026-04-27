import oracledb
import pandas as pd
from pathlib import Path

# Connects to Oracle
oracledb.init_oracle_client(lib_dir=r"C:\Users\panam\Downloads\instantclient_11_2")
USERNAME = "JWOLF8270_SCHEMA_THLR8"
PASSWORD = "FQG5ZL1!NPQ7uMC6Q7POLERRX1H9G0"
DSN = "db.freesql.com:1521/23ai_34ui2"
connection = oracledb.connect(user=USERNAME, password=PASSWORD, dsn=DSN)
cursor = connection.cursor()

# Loads the CSVs into DataFrames
data_path = Path(r"C:/Users/panam/data")
dfs = {
    "AIRLINE": pd.read_csv(data_path / "AIRLINE.csv"),
    "AIRPORT": pd.read_csv(data_path / "AIRPORT.csv"),
    "AIRCRAFT": pd.read_csv(data_path / "AIRCRAFT.csv"),
    "ROUTE": pd.read_csv(data_path / "ROUTE.csv"),
    "FLIGHT": pd.read_csv(data_path / "FLIGHT.csv"),
    "FLIGHT_DELAY": pd.read_csv(data_path / "FLIGHT_DELAY.csv"),
}

# Normalizes foreign keys before insertion into tables
def normalize_keys_and_timestamps(dfs):
    route_df = dfs["ROUTE"]
    flight_df = dfs["FLIGHT"]
    delay_df = dfs["FLIGHT_DELAY"]

    # Maps the origin to destination airport to the appropriate ROUTE_ID
    route_lookup = {
        f"{row['ORIGIN_AIRPORT']}_{row['DESTINATION_AIRPORT']}": row['ROUTE_ID']
        for _, row in route_df.iterrows()
    }
    # Fixes ROUTE_IDs, but keeps the original route if no issues are found, additionally fills empty routes with UNKNOWN_ROUTE
    flight_df["ROUTE_ID"] = flight_df["ROUTE_ID"].apply(lambda r: route_lookup.get(r, r if pd.notnull(r) else 'UNKNOWN_ROUTE'))

    # Converts timestamps to necessary from and replaces NaT with default placeholder
    for col in ["DEPARTURE_TIME", "ARRIVAL_TIME"]:
        flight_df[col] = pd.to_datetime(flight_df[col], errors="coerce")
        flight_df[col] = flight_df[col].fillna(pd.Timestamp("1970-01-01 00:00:00"))

    # Ensures that FLIGHT_ID and FLIGHT_NUMBER are formatted correctly before insertion into the table
    flight_df["FLIGHT_ID"] = flight_df["FLIGHT_ID"].astype(str)
    flight_df["FLIGHT_NUMBER"] = pd.to_numeric(flight_df["FLIGHT_NUMBER"], errors="coerce").fillna(0).astype(int)

    # Normalizes FLIGHT_DELAY.FLIGHT_ID by stripping the 'F' prefix
    delay_df["FLIGHT_ID"] = delay_df["FLIGHT_ID"].apply(lambda x: str(x).lstrip("F"))

    # Fills in missing numeric columns in delay_df
    delay_df["DELAY_SEQUENCE"] = pd.to_numeric(delay_df["DELAY_SEQUENCE"], errors="coerce").fillna(0).astype(int)
    delay_df["DELAY_MINUTES"] = pd.to_numeric(delay_df["DELAY_MINUTES"], errors="coerce").fillna(0).astype(int)

    dfs["FLIGHT"] = flight_df
    dfs["FLIGHT_DELAY"] = delay_df
    return dfs

# Cleans and normalizes the CSV data
dfs = normalize_keys_and_timestamps(dfs)

# Drops flights with missing aircraft IDs
flight_df = dfs["FLIGHT"]

flight_df["AIRCRAFT_ID"] = flight_df["AIRCRAFT_ID"].replace(r'^\s*$', None, regex=True)
flight_df = flight_df[flight_df["AIRCRAFT_ID"].notnull()]

dfs["FLIGHT"] = flight_df

# Drops flight delays linked to flights with missing aircraft IDs
delay_df = dfs["FLIGHT_DELAY"]

valid_flights = set(dfs["FLIGHT"]["FLIGHT_ID"].astype(str))
delay_df = delay_df[delay_df["FLIGHT_ID"].isin(valid_flights)]

dfs["FLIGHT_DELAY"] = delay_df

# Loads the CSV data into a table
def load_table_df(df, table_name, columns, numeric_columns=None, datetime_columns=None):
    print(f"\nLoading {table_name}...")
    for col in columns:
        if col not in df.columns:
            df[col] = None
    df = df[columns]

    # Cleans any string columns
    for col in columns:
        df[col] = df[col].apply(lambda x: str(x).strip() if pd.notnull(x) else None)

    # Converts numeric columns into appropriate data types
    if numeric_columns:
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Converts datetime columns into datetime objects
    if datetime_columns:
        for col in datetime_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Replaces NaN or NaT with None to avoid errors in compiling
    df = df.astype(object).where(pd.notnull(df), None)

    # Inserts into Oracle
    placeholders = ",".join([f":{i+1}" for i in range(len(columns))])
    sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"

    # Debugs rows to determine if any fail to insert into the table
    for row in df.values:
        try:
            cursor.execute(sql, tuple(row))
        except Exception as e:
            print("FAILED ROW:", row)
            print("ERROR:", e)
            return

    connection.commit()

    # Prints the loaded table and its number of rows
    print(f"Loaded {table_name} ({len(df)} rows)")

# Loads the tables in the proper order
load_table_df(dfs["AIRLINE"], "AIRLINE", ["AIRLINE_CODE", "AIRLINE_NAME", "HEADQUARTERS"])
load_table_df(dfs["AIRPORT"], "AIRPORT", ["AIRPORT_CODE", "AIRPORT_NAME", "CITY", "STATE", "COUNTRY", "TIMEZONE", "LATITUDE", "LONGITUDE"], numeric_columns=["LATITUDE", "LONGITUDE"])
load_table_df(dfs["AIRCRAFT"], "AIRCRAFT", ["AIRCRAFT_ID", "TAIL_NUMBER", "MODEL", "CAPACITY"], numeric_columns=["CAPACITY"])
load_table_df(dfs["ROUTE"], "ROUTE", ["ROUTE_ID", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT", "DISTANCE"], numeric_columns=["DISTANCE"])
load_table_df(dfs["FLIGHT"], "FLIGHT", ["FLIGHT_ID", "FLIGHT_NUMBER", "AIRLINE_CODE", "ROUTE_ID", "AIRCRAFT_ID", "DEPARTURE_TIME", "ARRIVAL_TIME", "STATUS"], numeric_columns=["FLIGHT_NUMBER"], datetime_columns=["DEPARTURE_TIME", "ARRIVAL_TIME"])
load_table_df(dfs["FLIGHT_DELAY"], "FLIGHT_DELAY", ["FLIGHT_ID", "DELAY_SEQUENCE", "DELAY_TYPE", "DELAY_MINUTES"], numeric_columns=["DELAY_SEQUENCE", "DELAY_MINUTES"])

# Closes the connection
cursor.close()
connection.close()
