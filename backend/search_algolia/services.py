from algoliasearch_django import raw_search
from netflix_titles.models import NetflixTitle


class AlgoliaService:
    @staticmethod
    def search(query, page=1, page_size=10, ordering=None):
        params = { "page": page, "hitsPerPage": page_size }

        # Handle ordering
        if ordering:
            if ordering.startswith("-"):  # Descending order
                params["sortFacetValuesBy"] = "alpha"  # Algolia does not support '-' prefix, must use facets
                params["facetFilters"] = [f"{ordering[1:]}:desc"]
            else:  # Ascending order
                params["facetFilters"] = [f"{ordering}:asc"]

        return raw_search(NetflixTitle, query, params)