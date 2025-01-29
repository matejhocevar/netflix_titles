from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from netflix_titles.models import NetflixTitle

@register(NetflixTitle)
class NetflixTitleIndex(AlgoliaIndex):
    fields = ("show_id", "type", "title", "director", "description", "cast", "release_year", "country", "description")
    settings = {
        "searchableAttributes": ["title", "director", "cast", "description"],
        "attributesForFaceting": ["release_year", "type", "country"]
    }