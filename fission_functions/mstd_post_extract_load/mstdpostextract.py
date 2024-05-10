import requests
from elasticsearch import Elasticsearch, helpers
from flask import jsonify, current_app


def fetch_posts_with_hashtag(mastodon_url, access_token, hashtag, min_id):
    """Fetch posts from Mastodon that are tagged with a specific hashtag."""
    url = f"{mastodon_url}/api/v1/timelines/tag/{hashtag}"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': 40, 'max_id': min_id} if min_id else {'limit': 40}
    all_posts = []

    while len(all_posts) < 400:
        response = requests.get(url, headers=headers, params=params, timeout=100)
        if response.status_code == 200:
            data = response.json()
            all_posts.extend(data)
            links = response.links
            url = links['next']['url'] if 'next' in links else None
            if not url:
                break
        else:
            current_app.logger.error(f"Failed to fetch posts for hashtag #{hashtag}: {response.status_code}")
            break

    return all_posts


def create_es_client():
    """Create and return an Elasticsearch client."""
    return Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )


def get_min_id_from_es(client, hashtag):
    """Retrieve the minimum ID from Elasticsearch for a given hashtag to avoid duplicates."""
    query = {
        "size": 1,
        "query": {
            "term": {"tag_search": hashtag}
        },
        "sort": [{"id": {"order": "asc"}}]
    }
    try:
        resp = client.search(index="mstd_social_tag_data", body=query)
        if resp['hits']['hits']:
            id_ = resp['hits']['hits'][0]['_source']['id']
            current_app.logger.info(f"Get min ID:{id_} Records found for hashtag{hashtag}")
            return id_
        current_app.logger.info(f"No existing records found for hashtag {hashtag}")
        return None
    except Exception as e:
        current_app.logger.error(f"Error fetching min_id from ES for hashtag {hashtag}: {str(e)}")
        return None


def pre_process(newly_extracted, hashtag):
    required_fields = ["id", "created_at", "language", "tags", "content"]
    processed_records = []
    for data in newly_extracted:
        clean_data = {field: data[field] for field in required_fields if field in data}
        clean_data['tag_search'] = hashtag
        processed_records.append(clean_data)
    return processed_records


def load_to_es(client, processed_records):
    if processed_records:
        try:
            helpers.bulk(client, processed_records, index="mstd_social_tag_data")
            current_app.logger.info(f"Loaded {len(processed_records)} records to Elasticsearch")
        except Exception as e:
            current_app.logger.error(f"Failed to load data to Elasticsearch: {str(e)}")


def main():
    mastodon_url = 'https://aus.social'
    access_token = 'hGhLLUOGUtQxWSJ44XRiXgMQEiFyO0Y_eSqQ0bNYwd4'
    hashtags = ['Melbourne']
    client = create_es_client()
    total_count = 0

    for hashtag in hashtags:
        min_id = get_min_id_from_es(client, hashtag)
        newly_extracted = fetch_posts_with_hashtag(mastodon_url, access_token, hashtag, min_id)
        processed_records = pre_process(newly_extracted, hashtag)
        load_to_es(client, processed_records)
        total_count += len(processed_records)

    return jsonify({"message": f"Successfully loaded {total_count} new posts.", "count": total_count}), 200
