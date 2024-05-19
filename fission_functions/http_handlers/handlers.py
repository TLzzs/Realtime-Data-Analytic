from flask import jsonify, request
from crimeservice import CrimeService
from weatherservice import WeatherService
from suburbservice import SuburbService
from sentimentservice import SentimentService



def get_all_suburbs():
    suburbs = SuburbService.get_all_suburbs()
    return jsonify(suburbs)


def get_crime_by_suburb():
    suburb_name = request.headers.get("X-Fission-Params-Suburb")
    suburb_info = SuburbService.get_suburb_info_by_name(suburb_name)
    lga_code = suburb_info["lga_code"]
    crime = CrimeService.get_crime_by_suburb(lga_code)
    return jsonify(crime)


def get_weather_by_suburb():
    suburb_name = request.headers.get("X-Fission-Params-Suburb")
    suburb_info = SuburbService.get_suburb_info_by_name(suburb_name)
    lga_code = suburb_info["lga_code"]
    weather = WeatherService.get_weather_by_suburb(lga_code)
    return jsonify(weather)


def get_suburb_crime_and_weather():
    suburb_name = request.headers.get("X-Fission-Params-Suburb")
    suburb_info = SuburbService.get_suburb_info_by_name(suburb_name)
    lga_code = suburb_info["lga_code"]
    crime = CrimeService.get_crime_by_suburb(lga_code)
    weather = WeatherService.get_weather_by_suburb(lga_code)
    crime_weather = {**crime, **weather, "suburb_name": suburb_name, "lga_code": lga_code}
    return jsonify(crime_weather)



def compare_sentiment_and_crime():
    year = int(request.headers.get("X-Fission-Params-Year"))
    result = SentimentService.compare_sentiment_and_crime(year)
    return jsonify(result)
