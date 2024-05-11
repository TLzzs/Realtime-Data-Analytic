from elasticsearch import Elasticsearch


class CrimeService:
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    @staticmethod
    def place_holder():
        return

    @staticmethod
    def get_crime_by_suburb(suburb_name):
        query = {
            "query": {
                "match": {
                    "suburb_name": suburb_name
                }
            }
        }
        result = CrimeService.client.search(index="crime_test", body=query)
        crime = result["hits"]["hits"][0]['_source']
        total_a_offences = crime["total_division_a_offences"]
        total_b_offences = crime["total_division_b_offences"]
        total_c_offences = crime["total_division_c_offences"]
        total_d_offences = crime["total_division_d_offences"]
        total_e_offences = crime["total_division_e_offences"]
        total_f_offences = crime["total_division_f_offences"]

        res = {
            "suburb_name": crime["suburb_name"],
            "total_offences": sum(
                [total_a_offences, total_b_offences, total_c_offences, total_d_offences, total_e_offences,
                 total_f_offences]),
            "total_a_offences": total_a_offences,
            "total_d_offences": total_d_offences
        }

        return res
