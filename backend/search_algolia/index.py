from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from netflix_titles.models import NetflixTitle

@register(NetflixTitle)
class NetflixTitleIndex(AlgoliaIndex):
    fields = ("show_id", "type", "title", "director", "description", "cast", "release_year", "country", "description")
    settings = {
        "searchableAttributes": ["title", "director", "cast", "description"],
        "replicas": [
            "netflix_titles_title_asc","netflix_titles_title_desc",
            "netflix_titles_type_asc", "netflix_titles_type_desc",
            "netflix_titles_director_asc", "netflix_titles_director_desc",
            "netflix_titles_duration_asc", "netflix_titles_duration_desc",
            "netflix_titles_country_asc", "netflix_titles_country_desc",
            "netflix_titles_release_year_asc", "netflix_titles_release_year_desc",
        ],
    }
    replica_settings = {
        "netflix_titles_title_asc": {"ranking": ["asc(title)"]},
        "netflix_titles_title_desc": {"ranking": ["desc(title)"]},
        "netflix_titles_type_asc": {"ranking": ["asc(type)"]},
        "netflix_titles_type_desc": {"ranking": ["desc(type)"]},
        "netflix_titles_director_asc": {"ranking": ["asc(director)"]},
        "netflix_titles_director_desc": {"ranking": ["desc(director)"]},
        "netflix_titles_duration_asc": {"ranking": ["asc(duration)"]},
        "netflix_titles_duration_desc": {"ranking": ["desc(duration)"]},
        "netflix_titles_country_asc": {"ranking": ["asc(country)"]},
        "netflix_titles_country_desc": {"ranking": ["desc(country)"]},
        "netflix_titles_release_year_asc": {"ranking": ["asc(release_year)"]},
        "netflix_titles_release_year_desc": {"ranking": ["desc(release_year)"]},
    }