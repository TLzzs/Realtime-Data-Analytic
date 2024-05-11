from elasticsearch import Elasticsearch


class WeatherService:
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    @staticmethod
    def get_all_weather():
        WeatherService.client.get_script_languages()
        return

    @staticmethod
    def get_weather_by_suburb(suburb_name):
        res = {
            "suburb_name": suburb_name,
            "average_temperature": 24,
            "average_precipitation": 99,
        }

        return res
