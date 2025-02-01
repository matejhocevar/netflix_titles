from elasticsearch import Elasticsearch
from elasticsearch_dsl.query import MultiMatch

from django.conf import settings
from .index import NetflixTitleDocument


class ElasticsearchService:
    def __init__(self):
        self.client = settings.ELASTICSEARCH_DSL["default"]["hosts"]
        self.index = "netflix_titles"

    def search(self, query, page=1, page_size=10):
        """
        Performs a search query in Elasticsearch.
        """

        search_query = NetflixTitleDocument.search().query(
            MultiMatch(query=query)
        )

        # Apply pagination
        search_results = search_query[(page - 1) * page_size : page * page_size].execute()

        print(search_results)

        return {
            "count": search_results.hits.total.value,
            "results": [hit.to_dict() for hit in search_results]
        }