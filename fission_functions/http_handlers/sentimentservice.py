from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
from textblob import TextBlob

class SentimentService:
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    social_index = "mstd_social_tag_data"
    crime_index = "sudo_crime" 

    @staticmethod
    def fetch_social_data():
        query = {
            "query": {
                "match_all": {}
            }
        }
        result = SentimentService.client.search(index=SentimentService.social_index, body=query)
        return result['hits']['hits']
    
    @staticmethod
    def fetch_crime_data(year):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "reference_period": {
                                    "gte": year,
                                    "lt": year + 1
                                }
                            }
                        }
                    ]
                }
            }
        }
        result = SentimentService.client.search(index=SentimentService.crime_index, body=query)
        return result['hits']['hits']

    @staticmethod
    def filter_by_year(data, id_type=2):
        filtered_data = []
        for item in data:
            # Assuming the ID is numeric and can be converted to an integer
            try:
                id_numeric = int(item['_id'])
                if id_type % 2 == 0 and id_numeric % 2 == 0:
                    content = item["_source"]['content']
                    soup = BeautifulSoup(content, 'html.parser')
                    content = soup.get_text()
                    filtered_data.append(content)
                elif id_type % 2 != 0 and id_numeric % 2 != 0:
                    content = item["_source"]['content']
                    soup = BeautifulSoup(content, 'html.parser')
                    content = soup.get_text()
                    print(f"The appended content is {content}")
                    filtered_data.append(content)
            except ValueError:
                continue  # Skip if the ID cannot be converted to an integer
            print(f"the data number after filter is: {len(filtered_data)}")
        return filtered_data

    @staticmethod
    def analyze_sentiment(content):
        blob = TextBlob(content)
        polarity = blob.sentiment.polarity
        print(f"The polarity score is: {polarity}")
        if polarity > 0:
            return "positive"
        elif polarity < 0:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def sentiment_counts(data):
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for content in data:
            sentiment = SentimentService.analyze_sentiment(content)
            sentiment_counts[sentiment] += 1
        return sentiment_counts
    
    @staticmethod
    def get_crime_data(year):
        crime_data = SentimentService.fetch_crime_data(year)
        total_crimes = len(crime_data)
        return total_crimes
    
    @staticmethod
    def compare_sentiment_and_crime(year):
        data_raw = SentimentService.fetch_social_data()
        filtered_data = SentimentService.filter_by_year(data_raw, year)
        sentiment_counts = SentimentService.sentiment_counts(filtered_data)
        total_crimes = SentimentService.get_crime_data(year)
        result = {
            "year": year,
            "sentiment_counts": sentiment_counts,
            "total_crimes": total_crimes
        }
        return result



