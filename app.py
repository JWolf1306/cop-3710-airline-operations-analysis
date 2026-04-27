import oracledb

conn = oracledb.connect(
    user="JWOLF8270_SCHEMA_THLR8",
    password="FQG5ZL1!NPQ7uMC6Q7POLERRX1H9G0",
    dsn="db.freesql.com:1521/23ai_34ui2"
)

cursor = conn.cursor()

print("Connected to database.\n")


def feature1():
    code = input("Enter Airline Code (e.g. AA): ")

    query = """
    SELECT f.FLIGHT_ID, f.FLIGHT_NUMBER, f.STATUS
    FROM FLIGHT f
    JOIN AIRLINE a ON f.AIRLINE_CODE = a.AIRLINE_CODE
    WHERE a.AIRLINE_CODE = :code
    """

    cursor.execute(query, {"code": code})
    results = cursor.fetchall()

    for row in results:
        print(f"Flight ID: {row[0]} | Number: {row[1]} | Status: {row[2]}")

def feature2():
    origin = input("Enter Origin Airport Code: ")
    dest = input("Enter Destination Airport Code: ")

    query = """
    SELECT f.FLIGHT_ID, f.FLIGHT_NUMBER, r.ORIGIN_AIRPORT, r.DESTINATION_AIRPORT
    FROM FLIGHT f
    JOIN ROUTE r ON f.ROUTE_ID = r.ROUTE_ID
    WHERE r.ORIGIN_AIRPORT = :origin
      AND r.DESTINATION_AIRPORT = :dest
    """

    cursor.execute(query, {"origin": origin, "dest": dest})
    results = cursor.fetchall()

    for row in results:
        print(f"Flight {row[0]}: {row[2]} → {row[3]}")


def feature3():
    flight_id = input("Enter Flight ID: ")

    query = """
    SELECT FLIGHT_ID, DELAY_TYPE, DELAY_MINUTES
    FROM FLIGHT_DELAY
    WHERE FLIGHT_ID = :flight_id
    """

    cursor.execute(query, {"flight_id": flight_id})
    results = cursor.fetchall()

    for row in results:
        print(f"Delay Type: {row[1]} | Minutes: {row[2]}")


def feature4():
    query = """
    SELECT a.AIRLINE_NAME, COUNT(f.FLIGHT_ID)
    FROM AIRLINE a
    LEFT JOIN FLIGHT f ON a.AIRLINE_CODE = f.AIRLINE_CODE
    GROUP BY a.AIRLINE_NAME
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(f"{row[0]}: {row[1]} flights")


def feature5():
    query = """
    SELECT f.FLIGHT_ID, ac.MODEL, ac.CAPACITY
    FROM FLIGHT f
    JOIN AIRCRAFT ac ON f.AIRCRAFT_ID = ac.AIRCRAFT_ID
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(f"Flight {row[0]} uses {row[1]} (Capacity: {row[2]})")


def menu():
    print("\n===== Airline Analysis System =====")
    print("1. View Flights by Airline")
    print("2. View Flights for Route")
    print("3. View Flight Delays")
    print("4. Flights per Airline")
    print("5. Aircraft per Flight")
    print("6. Exit")


while True:
    menu()
    choice = input("Choose option: ")

    if choice == '1':
        feature1()
    elif choice == '2':
        feature2()
    elif choice == '3':
        feature3()
    elif choice == '4':
        feature4()
    elif choice == '5':
        feature5()
    elif choice == '6':
        break
    else:
        print("Invalid choice.")

conn.close()
