from elasticsearch import Elasticsearch
from elasticsearch_dsl.query import MultiMatch

from django.conf import settings
from .index import NetflixTitleDocument


class ElasticsearchService:
    def __init__(self):
        self.client = settings.ELASTICSEARCH_DSL["default"]["hosts"]
        self.index = "netflix_titles"

    def search(self, query, page=1, page_size=10, ordering=None):
        """
        Performs a search query in Elasticsearch.
        """

        search_query = NetflixTitleDocument.search().query(
            MultiMatch(query=query)
        )

        if ordering:
            order_field = ordering.lstrip('-')  # Remove '-' prefix for descending
            order_direction = "desc" if ordering.startswith('-') else "asc"
            search_query = search_query.sort({order_field: {"order": order_direction}})

        # Apply pagination
        search_results = search_query[(page - 1) * page_size : page * page_size].execute()

        total_results = search_results.hits.total.value
        total_pages = (total_results + page_size - 1) // page_size

        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "count": total_results,
            "page": page,
            "total_pages": total_pages,
            "next": next_page,
            "previous": prev_page,
            "results": [hit.to_dict() for hit in search_results],
        }