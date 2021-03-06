"""
Main server routes
"""
import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from api import settings
from api.flaskr.hiking import HikingApi
from api.flaskr.geocoding_api import geocode
from api.flaskr.weather import get_current_weather
from api.flaskr.cold_weather import find_closest_station, find_coldest_weather

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_CONNECTION_STING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from api.flaskr.model import TrailModel

@app.route('/lat-lng', methods=['POST'])
def lat_lng():
    """
    Geocoding API endpoint
    :return: lat and long given a city name
    """
    name = request.get_json(force=True)
    city_name = name['city_name']
    lat_lng = geocode(city_name)
    if lat_lng is None:
        return '500'
    else:
        lat_lng_dict = { 'lat':lat_lng[0], 'lng':lat_lng[1] }
        return json.dumps(lat_lng_dict)


@app.route('/trails', methods=['POST'])
def get_trails():
    """
    Trails list API endpoint
    :return: list of nearby trails to a given lat and long
    """
    name_and_distance = request.get_json(force=True)
    city_name = name_and_distance['city_name']
    max_distance = name_and_distance['distance']
    lat_lng = geocode(city_name)
    if lat_lng is None:
        return '500'
    hiking_api = HikingApi()
    trails = hiking_api.get_trails(lat_lng[0], lat_lng[1], max_distance)
    trails_dicts = [trail.as_dict() for trail in trails]
    return json.dumps(trails_dicts)

@app.route('/weather', methods=['POST'])
def get_weather():
    """
    Weather API endpoint
    :return: weather forecast for a location given lat and long
    """
    lat_and_lng = request.get_json(force=True)
    lat = lat_and_lng['lat']
    lng = lat_and_lng['lng']
    return get_current_weather(lat, lng)

@app.route('/coldest-weather', methods=['POST'])
def get_cold_weather():
    """
    Coldest weather API endpoint
    :return: coldest weather in the past 10 years, adjusted for altitude, for a given lat and long
    """
    FEET_PER_METER = 3.28084
    lat_lng_day_month_maxElev = request.get_json(force=True)
    lat = lat_lng_day_month_maxElev['lat']
    lng = lat_lng_day_month_maxElev['lng']
    day = lat_lng_day_month_maxElev['day']
    month = lat_lng_day_month_maxElev['month']
    elev = lat_lng_day_month_maxElev['maxElev']
    closest_station = find_closest_station(float(lat), float(lng))
    day_formatted = "{:02d}".format(day)
    month_formatted = "{:02d}".format(month)
    coldest_weather = find_coldest_weather(day_formatted, month_formatted, closest_station['wban'], closest_station['usaf'])
    altitude_adjustment = ((float(elev)-float(closest_station['elevation'])*FEET_PER_METER)/1000)*3.5
    coldest_weather -= altitude_adjustment
    return json.dumps(round(coldest_weather))

