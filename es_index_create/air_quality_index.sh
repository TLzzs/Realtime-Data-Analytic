curl -XPUT -k 'https://127.0.0.1:9200/observations' \
   --user 'elastic:elastic' \
   --header 'Content-Type: application/json' \
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
    "properties": {
      "geometry": {
        "properties": {
          "coordinates": {"type": "geo_point"},
          "type": {"type": "keyword"}
        }
      },
      "siteHealthAdvices": {
        "type": "nested",
        "properties": {
          "averageValue": {"type": "float"},
          "healthAdvice": {"type": "keyword"},
          "healthAdviceColor": {"type": "keyword"},
          "healthCode": {"type": "keyword"},
          "healthParameter": {"type": "keyword"},
          "since": {"type": "date"},
          "unit": {"type": "keyword"},
          "until": {"type": "date"}
        }
      },
      "siteID": {"type": "keyword"},
      "siteName": {"type": "text"},
      "siteType": {"type": "keyword"}
    }
  }
}' | jq '.'