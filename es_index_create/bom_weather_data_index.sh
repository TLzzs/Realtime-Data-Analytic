curl -XPUT -k 'https://127.0.0.1:9200/bom_weather_data' \
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
    "dynamic": "false",
    "properties": {
      "station_id": {"type": "keyword"},
      "station_name":  {"type": "keyword"},
      "state": {"type": "keyword"},
      "wmo": {"type": "integer"},
      "name": {"type": "keyword"},
      "history_product": {"type": "keyword"},
      "local_date_time": {"type": "text"},
      "local_date_time_full": {
        "type": "date",
        "format": "yyyyMMddHHmmss"
      },
      "aifstime_utc": {"type": "keyword"},
      "lat": {"type": "float"},
      "lon": {"type": "float"},
      "apparent_t": {"type": "float"},
      "cloud": {"type": "text"},
      "cloud_base_m": {"type": "integer"},
      "cloud_oktas": {"type": "integer"},
      "cloud_type": {"type": "text"},
      "cloud_type_id": {"type": "keyword"},
      "delta_t": {"type": "float"},
      "gust_kmh": {"type": "integer"},
      "gust_kt": {"type": "integer"},
      "air_temp": {"type": "float"},
      "dewpt": {"type": "float"},
      "press": {"type": "float"},
      "press_msl": {"type": "float"},
      "press_qnh": {"type": "float"},
      "press_tend": {"type": "text"},
      "rain_trace": {"type": "text"},
      "rel_hum": {"type": "integer"},
      "sea_state": {"type": "text"},
      "swell_dir_worded": {"type": "text"},
      "swell_height": {"type": "float"},
      "swell_period": {"type": "integer"},
      "vis_km": {"type": "text"},
      "weather": {"type": "text"},
      "wind_dir": {"type": "keyword"},
      "wind_spd_kmh": {"type": "integer"},
      "wind_spd_kt": {"type": "integer"}
    }
  }
}' | jq '.'