from algoliasearch_django import raw_search
from netflix_titles.models import NetflixTitle


class AlgoliaService:
    @staticmethod
    def search(query, page=1, page_size=10, ordering=None):
        params = { "page": page, "hitsPerPage": page_size }

        # Handle ordering using replicas
        ordering_map = {
            "title": "netflix_titles_title_asc",
            "-title": "netflix_titles_title_desc",
            "type": "netflix_titles_type_asc",
            "-type": "netflix_titles_type_desc",
            "director": "netflix_titles_director_asc",
            "-director": "netflix_titles_director_desc",
            "duration": "netflix_titles_duration_asc",
            "-duration": "netflix_titles_duration_desc",
            "country": "netflix_titles_country_asc",
            "-country": "netflix_titles_country_desc",
            "release_year": "netflix_titles_release_year_asc",
            "-release_year": "netflix_titles_release_year_desc",
        }

        # If ordering is specified, use the corresponding replica
        if ordering and ordering in ordering_map:
            params["indexName"] = ordering_map[ordering]

        return raw_search(NetflixTitle, query, params)