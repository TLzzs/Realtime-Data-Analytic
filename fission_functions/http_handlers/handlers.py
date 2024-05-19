from flask import jsonify, request, make_response
from crimeservice import CrimeService
from weatherservice import WeatherService
from suburbservice import SuburbService
from sentimentservice import SentimentService


def get_all_suburbs():
    suburbs = SuburbService.get_all_suburbs()
    return make_response(jsonify(suburbs), 200)


def get_crime_by_suburb():
    suburb_name = request.headers.get("X-Fission-Params-Suburb")
    suburb_info = SuburbService.get_suburb_info_by_name(suburb_name)
    
    if not suburb_info:
        return make_response(jsonify({"error": "Suburb not found"}), 404)
    
    lga_code = suburb_info["lga_code"]
    crime = CrimeService.get_crime_by_suburb(lga_code)
    return make_response(jsonify(crime), 200)


def get_weather_by_suburb():
    suburb_name = request.headers.get("X-Fission-Params-Suburb")
    suburb_info = SuburbService.get_suburb_info_by_name(suburb_name)
    
    if not suburb_info:
        return make_response(jsonify({"error": "Suburb not found"}), 404)
    
    lga_code = suburb_info["lga_code"]
    weather = WeatherService.get_weather_by_suburb(lga_code)
    return make_response(jsonify(weather), 200)


def get_suburb_crime_and_weather():
    suburb_name = request.headers.get("X-Fission-Params-Suburb")
    suburb_info = SuburbService.get_suburb_info_by_name(suburb_name)
    
    if not suburb_info:
        return make_response(jsonify({"error": "Suburb not found"}), 404)
    
    lga_code = suburb_info["lga_code"]
    crime = CrimeService.get_crime_by_suburb(lga_code)
    weather = WeatherService.get_weather_by_suburb(lga_code)
    crime_weather = {**crime, **weather, "suburb_name": suburb_name, "lga_code": lga_code}
    return make_response(jsonify(crime_weather), 200)


def compare_sentiment_and_crime():
    year = request.headers.get("X-Fission-Params-Year")
    
    if not year:
        return make_response(jsonify({"error": "Year parameter is required"}), 400)
    
    try:
        year = int(year)
    except ValueError:
        return make_response(jsonify({"error": "Year parameter must be an integer"}), 400)
    
    result = SentimentService.compare_sentiment_and_crime(year)
    return make_response(jsonify(result), 200)
