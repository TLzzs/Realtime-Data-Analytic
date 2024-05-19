from elasticsearch import Elasticsearch


class CrimeService:
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    index_name = "sudo_crime"

    @staticmethod
    def get_all_crimes():
        query = {
            "query": {
                "match_all": {}
            }
        }
        result = CrimeService.client.search(index=CrimeService.index_name, body=query)
        crimes = result["hits"]["hits"]

        return crimes

    @staticmethod
    def get_crime_by_suburb(lga_code):
        query = {
            "query": {
                "match": {
                    "lga_code11": lga_code
                }
            }
        }
        result = CrimeService.client.search(index=CrimeService.index_name, body=query)
        if len(result["hits"]["hits"]) == 0:
            return None
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
            "total_b_offences": total_b_offences
        }

        return res
