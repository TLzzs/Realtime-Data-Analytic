from flask import jsonify, request
from crimeservice import CrimeService
from weatherservice import WeatherService

def get_crime_by_suburb():
    suburb_name = request.headers.get("X-Fission-Params-Suburb")
    crime = CrimeService.get_crime_by_suburb(suburb_name)
    return jsonify(crime)


def get_weather_by_suburb():
    #suburb_name = request.headers.get("X-Fission-Params-Suburb")
    suburb_name = "Alpine"
    weather = WeatherService.get_weather_by_suburb(suburb_name)
    return jsonify(weather)

def get_suburb_crime_and_weather():
    #suburb_name = request.headers.get("X-Fission-Params-Suburb")
    suburb_name = "Alpine"
    crime = CrimeService.get_crime_by_suburb(suburb_name)
    weather = WeatherService.get_weather_by_suburb(suburb_name)
    crime_weather = {**crime, **weather}
    return jsonify(crime_weather)
