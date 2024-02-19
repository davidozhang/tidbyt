from flask import Flask, request
from FlightRadar24 import FlightRadar24API

app = Flask(__name__)
fr_api = FlightRadar24API()

FLIGHTS_PARAM = 'flights'
LAT_PARAM = 'lat'
LNG_PARAM = 'lng'
RADIUS_PARAM = 'radius'
AIRCRAFT_CODE_PARAM = 'aircraft_code'
CALLSIGN_PARAM = 'callsign'
DESTINATION_AIRPORT_IATA_PARAM = 'destination_airport_iata'
ORIGIN_AIRPORT_IATA_PARAM = 'origin_airport_iata'

@app.route('/flights')
def flights_overhead():
    d = {FLIGHTS_PARAM: []}

    if not request.args.get(LAT_PARAM) and not request.args.get(LNG_PARAM) and not request.args.get(RADIUS_PARAM):
        return d

    lat = float(request.args.get(LAT_PARAM))
    lng = float(request.args.get(LNG_PARAM))
    radius = float(request.args.get(RADIUS_PARAM))
    bounds = fr_api.get_bounds_by_point(lat, lng, radius)
    flights = fr_api.get_flights(bounds=bounds)

    if not flights:
        return d

    filtered_flights = []
    for flight in flights:
        if flight.callsign and flight.altitude > 0 and flight.origin_airport_iata and flight.destination_airport_iata:
                filtered_flights.append(flight)

    for flight in filtered_flights:
        d[FLIGHTS_PARAM].append({
            AIRCRAFT_CODE_PARAM: flight.aircraft_code,
            CALLSIGN_PARAM: flight.callsign,
            DESTINATION_AIRPORT_IATA_PARAM: flight.destination_airport_iata,
            ORIGIN_AIRPORT_IATA_PARAM: flight.origin_airport_iata
        })

    return d
