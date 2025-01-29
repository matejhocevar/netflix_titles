from elasticsearch import Elasticsearch

class ElasticsearchService:
    def __init__(self):
        self.client = Elasticsearch(["http://localhost:9200"])
        self.index = "netflix_titles"

    def search(self, query, page=1, page_size=10):
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description", "cast", "director"]
                }
            },
            "from": (page - 1) * page_size,
            "size": page_size
        }
        response = self.client.search(index=self.index, body=body)
        return [hit["_source"] for hit in response["hits"]["hits"]]