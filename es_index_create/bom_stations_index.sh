curl -X PUT "https://elasticsearch-master.elastic.svc.cluster.local:9200/bom_stations" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "station_id": {"type": "keyword"},
      "station_name": {"type": "text"},
      "state": {"type": "keyword"},
      "url": {"type": "keyword"}
    }
  }
}'