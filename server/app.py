import os
import requests

from datetime import datetime
from dotenv import load_dotenv
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

STOP_ID_PARAM = 'stop_id'
OBA_API_KEY_PARAM = 'oba_api_key'
ROUTE_PARAM = 'route'
ARRIVAL_TIME_PARAM = 'arrival_time'
ARRIVAL_TIMES_PARAM = 'arrival_times'
STOP_NAME_PARAM = 'stop_name'

OBA_ADS_API = 'https://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop'

@app.route('/flights')
def flights_api():
    result = {FLIGHTS_PARAM: []}

    if not request.args.get(LAT_PARAM) or not request.args.get(LNG_PARAM) or not request.args.get(RADIUS_PARAM):
        return result

    lat = float(request.args.get(LAT_PARAM))
    lng = float(request.args.get(LNG_PARAM))
    radius = float(request.args.get(RADIUS_PARAM))
    bounds = fr_api.get_bounds_by_point(lat, lng, radius)
    flights = fr_api.get_flights(bounds=bounds)

    if not flights:
        return result

    for flight in flights:
        if not flight.callsign:
            continue

        if request.args.get(LAT4DIR_PARAM) and request.args.get(LNG4DIR_PARAM):
            bearing = Geodesic.WGS84.Inverse(
                float(request.args.get(LAT4DIR_PARAM)),
                float(request.args.get(LNG4DIR_PARAM)),
                flight.latitude,
                flight.longitude
            )['azi1']
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

        destination_airport_iata = flight.destination_airport_iata if flight.destination_airport_iata else 'N/A'
        origin_airport_iata = flight.origin_airport_iata if flight.origin_airport_iata else 'N/A'

        result[FLIGHTS_PARAM].append({
            AIRCRAFT_CODE_PARAM: flight.aircraft_code,
            ALTITUDE_PARAM: flight.get_altitude(),
            CALLSIGN_PARAM: flight.callsign,
            DESTINATION_AIRPORT_IATA_PARAM: destination_airport_iata,
            DIRECTION_PARAM: direction,
            GROUND_SPEED_PARAM: flight.get_ground_speed(),
            HEADING_PARAM: flight.get_heading(),
            LAT_PARAM: flight.latitude,
            LNG_PARAM: flight.longitude,
            ON_GROUND_PARAM: flight.on_ground == 1,
            ORIGIN_AIRPORT_IATA_PARAM: origin_airport_iata,
            VERTICAL_SPEED_PARAM: flight.get_vertical_speed()
        })

    return result

@app.route('/transit')
def transit_api():
    load_dotenv('/home/davidozhang/tidbyt/server/.env')

    oba_api_key = os.getenv('OBA_API_KEY')
    result = {ARRIVAL_TIMES_PARAM: []}

    if not request.args.get(STOP_ID_PARAM):
        return result

    stop_id = request.args.get(STOP_ID_PARAM)

    adfs = requests.get(
        f'{OBA_ADS_API}/{stop_id}.json?key={oba_api_key}').json()

    if 'data' not in adfs:
        return result

    ads = adfs['data']['entry']['arrivalsAndDepartures']
    stops = adfs['data']['references']['stops']

    for stop in stops:
        if stop['id'] == stop_id:
            result[STOP_NAME_PARAM] = stop['name']
            break

    for ad in ads:
        if not ad['predicted']:
            continue
        predicted_arrival_time_ms = ad['predictedArrivalTime']
        route_short_name = ad['routeShortName']
        td = datetime.fromtimestamp(int(predicted_arrival_time_ms)/1000) - datetime.now()
        arrival_time = td.seconds/60

        result[ARRIVAL_TIMES_PARAM].append({
            ROUTE_PARAM: route_short_name,
            ARRIVAL_TIME_PARAM: arrival_time
        })

    return result
