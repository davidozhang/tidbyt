from flask import Flask, request
from FlightRadar24 import FlightRadar24API
from geographiclib.geodesic import Geodesic

app = Flask(__name__)
fr_api = FlightRadar24API()
flight_tracker = fr_api.get_flight_tracker_config()
flight_tracker.limit = 1
fr_api.set_flight_tracker_config(flight_tracker)

AIRCRAFT_CODE_PARAM = 'aircraft_code'
ALTITUDE_PARAM = 'altitude'
CALLSIGN_PARAM = 'callsign'
DESTINATION_AIRPORT_IATA_PARAM = 'destination_airport_iata'
DIRECTION_PARAM = 'direction'
FLIGHTS_PARAM = 'flights'
GROUND_SPEED_PARAM = 'ground_speed'
HEADING_PARAM = 'heading'
LAT_PARAM = 'lat'
LNG_PARAM = 'lng'
LAT4DIR_PARAM = 'lat4dir'
LNG4DIR_PARAM = 'lng4dir'
ON_GROUND_PARAM = 'on_ground'
ORIGIN_AIRPORT_IATA_PARAM = 'origin_airport_iata'
RADIUS_PARAM = 'radius'
VERTICAL_SPEED_PARAM = 'vertical_speed'

@app.route('/flights')
def flights():
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

    for flight in flights:
        if flight.callsign and (flight.origin_airport_iata or flight.destination_airport_iata):
            if request.args.get(LAT4DIR_PARAM) and request.args.get(LNG4DIR_PARAM):
                bearing = Geodesic.WGS84.Inverse(
                    float(request.args.get(LAT4DIR_PARAM)),
                    float(request.args.get(LNG4DIR_PARAM)),
                    flight.latitude,
                    flight.longitude)['azi1']
            else:
                bearing = Geodesic.WGS84.Inverse(lat, lng, flight.latitude, flight.longitude)['azi1']

            if bearing == 0 or bearing == 360:
                direction = 'N'
            elif 0 < bearing < 80:
                direction = 'NE'
            elif 80 <= bearing <= 100:
                direction = 'N'
            elif 100 < bearing < 170:
                direction = 'SE'
            elif 170 <= bearing <= 190:
                direction = 'S'
            elif 190 < bearing < 260:
                direction = 'SW'
            elif 260 <= bearing <= 280:
                direction = 'W'
            else:
                direction = 'NW'

            d[FLIGHTS_PARAM].append({
                AIRCRAFT_CODE_PARAM: flight.aircraft_code,
                ALTITUDE_PARAM: flight.get_altitude(),
                CALLSIGN_PARAM: flight.callsign,
                DESTINATION_AIRPORT_IATA_PARAM: flight.destination_airport_iata if flight.destination_airport_iata else 'N/A',
                DIRECTION_PARAM: direction,
                GROUND_SPEED_PARAM: flight.get_ground_speed(),
                HEADING_PARAM: flight.get_heading(),
                LAT_PARAM: flight.latitude,
                LNG_PARAM: flight.longitude,
                ON_GROUND_PARAM: flight.on_ground == 1,
                ORIGIN_AIRPORT_IATA_PARAM: flight.origin_airport_iata if flight.origin_airport_iata else 'N/A',
                VERTICAL_SPEED_PARAM: flight.get_vertical_speed()
            })

    return d
