# COP 3710: Airline Operations Analysis
## Project Scope
The project lies within the domain of transportation analytics, specificially aviation operation analytics. The
primary goal of this project is to analyze U.S. flight data to determine and understand causes behind flight delays.
With these delay causes determined, this project will aid in improving efficiency within airline operations and
airports.
## Intended Users
The intended users of this database are airline operation analysts and airport management, as they will attempt
to optimize traffic efficiency for arriving and departing flights by minimalizing delays. Additional users include
travelers looking to trends within flight delays and researchers studying data on flight operations.
## Data Sources
- Kaggle: 2015 Flight Delays and Cancellations Dataset - https://www.kaggle.com/datasets/usdot/flight-delays
## Database Application
The database application consists of the following entities:
- AIRLINE (Strong Entity)
- AIRPORT (Strong Entity)
- AIRCRAFT (Strong Entity)
- FLIGHT (Strong Entity)
- FLIGHT_DELAY (Weak Entity)
- ROUTE (Associative Entity)

The following relationships are used in the design of the database to best represent aviation operations:
- One-to-Many: One airline operates many flights.
- One-to-One: Each flight is assigned a specific aircraft.
- Many-to-Many: Airports are connected through routes, allowing multiple flights between origin and destination pairs.

A notable design component is the FLIGHT_DELAY entity, which is a weak entity. Given that delay events require a flight to exist, a composite primary key consisting of FLIGHT_ID and DELAY_SEQUENCE is used to identify these delay events. As a result, one flight is able to have multiple categorized delay events. Additionally, the ROUTE entity is used as an associative entity between airports to resolve the many-to-many relationship between origin and destination airports, while providing analysis of routes between airports.

## Final Database Design
Below is the final database design for this project. This design was chosen given its efficiency in covering all necessary info relevant to monitoring airline operations, in addition to its satisfaction of BNCF conditions.

<img width="1225" height="416" alt="Screenshot 2026-03-02 232448" src="https://github.com/user-attachments/assets/12f17a56-0719-46b5-9e99-fffb7842a986" />

## Applications Features
There are five prominent features provided within the application:
- View flights by airline: Users are able to search and view flights by entering an airline code.
- View flights per route: Users are able to search and view flights by entering a specific origin and destination airport.
- View flight delays: Users are able to search for flight delays by flight ID.
- Flights per airline: This shows number of flights for each airline.
- Aircraft per flight: This lists the aircraft model used on each flight.
