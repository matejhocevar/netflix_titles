from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.field import Keyword, Text, Integer

from netflix_titles.models import NetflixTitle


@registry.register_document
class NetflixTitleDocument(Document):
    """
    Elasticsearch index for Netflix Titles
    """

    class Index:
        name = "netflix_titles"  # Index name in Elasticsearch
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = NetflixTitle
        fields = [
            "show_id",
            "type",
            "title",
            "director",
            "cast",
            "country",
            "release_year",
            "rating",
            "duration",
            "description",
        ]