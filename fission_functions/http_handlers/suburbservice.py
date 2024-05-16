from elasticsearch import Elasticsearch


class SuburbService:
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    # stands for local government area
    index_name = "lga"

    @staticmethod
    def get_all_suburbs():
        query = {
            "query": {
                "match_all": {}
            }
        }
        result = SuburbService.client.search(index=SuburbService.index_name, body=query)
        suburbs = result["hits"]["hits"]
        res = list(
            map(lambda s: {
                "suburb_name": s["_source"]["Official Name Local Government Area"],
                "lga_code": s["_source"]["Official Code Local Government Area"],
                "geo_point": s["_source"]["Geo Point"]
            }, suburbs)
        )
        return res

    @staticmethod
    def get_suburb_info_by_name(suburb_name):
        query = {
            "query": {
                "match": {
                    "Official Name Local Government Area": suburb_name
                }
            }
        }
        result = SuburbService.client.search(index=SuburbService.index_name, body=query)
        suburb = result["hits"]["hits"]
        if len(suburb) == 0:
            return None
        else:
            res = {
                "suburb_name": suburb[0]["_source"]["Official Name Local Government Area"],
                "lga_code": suburb[0]["_source"]["Official Code Local Government Area"],
                "geo_point": suburb[0]["_source"]["Geo Point"]
            }
            return res
