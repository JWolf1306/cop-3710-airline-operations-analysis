import pandas as pd
import os

OUTPUT_DIR = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Data cleaning function
def clean_df(df):
    df = df.drop_duplicates()

    # Strips whitespace
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()

    # Replaces NaN with None
    df = df.where(pd.notnull(df), None)

    return df


# AIRLINE Table
airline = pd.read_csv(r"C:\Users\panam\Downloads\data\AIRLINE.csv")

airline = airline.rename(columns={
    "IATA_CODE": "AIRLINE_CODE",
    "AIRLINE": "AIRLINE_NAME"
})

airline["HEADQUARTERS"] = None

airline = airline[["AIRLINE_CODE", "AIRLINE_NAME", "HEADQUARTERS"]]

airline = clean_df(airline)
airline.to_csv(f"{OUTPUT_DIR}/AIRLINE.csv", index=False)


# AIRPORT Table
airport = pd.read_csv(r"C:\Users\panam\Downloads\data\AIRPORT.csv")

airport = airport.rename(columns={
    "IATA_CODE": "AIRPORT_CODE",
    "AIRPORT": "AIRPORT_NAME"
})

airport["TIMEZONE"] = "Unknown"

airport = airport[
    ["AIRPORT_CODE", "AIRPORT_NAME", "CITY", "STATE",
     "COUNTRY", "TIMEZONE", "LATITUDE", "LONGITUDE"]
]

airport = clean_df(airport)
airport.to_csv(f"{OUTPUT_DIR}/AIRPORT.csv", index=False)


# AIRCRAFT Table
aircraft = pd.read_csv(r"C:\Users\panam\Downloads\data\AIRCRAFT.csv")

aircraft = clean_df(aircraft)

aircraft.to_csv(f"{OUTPUT_DIR}/AIRCRAFT.csv", index=False)


# ROUTE Table
route = pd.read_csv(r"C:\Users\panam\Downloads\data\ROUTE.csv")

route = clean_df(route)

route.to_csv(f"{OUTPUT_DIR}/ROUTE.csv", index=False)


# Format Time fix function
def format_time(val):
    if pd.isna(val):
        return None
    val = str(val).zfill(4)
    return f"2015-01-01 {val[:2]}:{val[2:]}:00"


# FLIGHT Table
flight = pd.read_csv(r"C:\Users\panam\Downloads\data\FLIGHT.csv", dtype={"ORIGIN_AIRPORT": str, "DESTINATION_AIRPORT": str}, low_memory=False)

# Renames the columns to match schema
flight = flight.rename(columns={
    "AIRLINE": "AIRLINE_CODE",
    "TAIL_NUMBER": "AIRCRAFT_ID"
})

# Creates FLIGHT_ID column
flight["FLIGHT_ID"] = range(1, len(flight) + 1)

# Create ROUTE_ID from origin + destination
flight["ROUTE_ID"] = (
    flight["ORIGIN_AIRPORT"].astype(str) + "_" +
    flight["DESTINATION_AIRPORT"].astype(str)
)

# Creates a STATUS row column
def get_status(row):
    if row["CANCELLED"] == 1:
        return "Cancelled"
    elif row["DIVERTED"] == 1:
        return "Diverted"
    else:
        return "Completed"

flight["STATUS"] = flight.apply(get_status, axis=1)

# Fixes the timestamps for the flight
flight["DEPARTURE_TIME"] = flight["DEPARTURE_TIME"].apply(format_time)
flight["ARRIVAL_TIME"] = flight["ARRIVAL_TIME"].apply(format_time)

# Selects the final schema columns
flight = flight[[
    "FLIGHT_ID", "FLIGHT_NUMBER", "AIRLINE_CODE",
    "ROUTE_ID", "AIRCRAFT_ID",
    "DEPARTURE_TIME", "ARRIVAL_TIME", "STATUS"
]]

# Clean and saves the dataset
flight = clean_df(flight)
flight.to_csv(f"{OUTPUT_DIR}/FLIGHT.csv", index=False)


# FLIGHT_DELAY Table
delay = pd.read_csv(r"C:\Users\panam\Downloads\data\FLIGHT_DELAY.csv")

delay = clean_df(delay)

delay.to_csv(f"{OUTPUT_DIR}/FLIGHT_DELAY.csv", index=False)