from flask import Flask
from FlightRadar24 import FlightRadar24API

app = Flask(__name__)
fr_api = FlightRadar24API()
bounds = fr_api.get_bounds_by_point(47.712380, -122.316400, 5000)

@app.route('/flights-overhead')
def flights_overhead():
    flights = fr_api.get_flights(bounds=bounds)
    d = {'flights': []}

    if not flights:
        print('No flights received')
        return d

    print(f'Flights received {flights}')

    filtered_flights = []
    for flight in flights:
        if flight.callsign and flight.altitude > 0 and flight.origin_airport_iata and flight.destination_airport_iata:
                filtered_flights.append(flight)

    for flight in filtered_flights:
        d['flights'].append({
            'aircraft_code': flight.aircraft_code,
            'altitude': flight.altitude,
            'callsign': flight.callsign,
            'destination_airport_iata': flight.destination_airport_iata,
            'flight_level': flight.get_flight_level(),
            'ground_speed': flight.ground_speed,
            'heading': flight.heading,
            'origin_airport_iata': flight.origin_airport_iata
        })

    return d
