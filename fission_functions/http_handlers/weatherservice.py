from elasticsearch import Elasticsearch

class WeatherService:

    @staticmethod
    def get_weather_by_suburb(suburb_name):
       
        res = {
            "suburb_name": suburb_name,
            "average_temperature": 24,
            "average_precipitation": 99,
        }

        return res
