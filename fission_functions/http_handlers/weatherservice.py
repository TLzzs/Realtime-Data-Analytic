from elasticsearch import Elasticsearch


class WeatherService:
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    index_name = "bom_weather_data"

    @staticmethod
    def get_suburb_average_temp(lga_code):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": "lga_code"
                            }
                        },
                        {
                            "term": {
                                "lga_code": lga_code
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "average_temp": {
                    "avg": {
                        "field": "air_temp"
                    }
                }
            }
        }

        result = WeatherService.client.search(index=WeatherService.index_name, body=query)
        res = {
            "average_temp": result["aggregations"]["average_temp"]["value"]
        }
        return res

    @staticmethod
    def get_suburb_average_rain(lga_code):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": "lga_code"
                            }
                        },
                        {
                            "term": {
                                "lga_code": lga_code
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "average_rain": {
                    "avg": {
                        "script": {
                            "source": "Double.parseDouble(doc['rain_trace'].value)"
                        }
                    }
                }
            }
        }
        result = WeatherService.client.search(index=WeatherService.index_name, body=query)
        res = {
            "average_rain": result["aggregations"]["average_rain"]["value"]
        }
        return res

    @staticmethod
    def get_weather_by_suburb(lga_code):
        temp = WeatherService.get_suburb_average_temp(lga_code)
        rain = WeatherService.get_suburb_average_rain(lga_code)
        res = {
            **temp, **rain
        }

        return res
