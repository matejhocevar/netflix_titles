from webbrowser import open_new

from rest_framework.response import Response
from netflix_titles.views import NetflixTitleViewSet
from .services import AlgoliaService


class AlgoliaSearchViewSet(NetflixTitleViewSet):
    """
    Extends NetflixTitleViewSet but modifies search behavior to use Algolia.
    """

    def get_queryset(self):
        """
        Prevents Django ORM queries when Algolia is handling search.
        Returns default queryset when no search query is provided.
        """
        query = self.request.GET.get("search", "").strip()
        if query:
            return self.queryset.none()
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        """
        Uses Algolia for searching and updates Django's pagination format.
        """
        query = request.GET.get("search", "")
        page = int(request.GET.get("page", 1)) - 1  # Algolia pages are 0-based
        page_size = int(request.GET.get("page_size", 10))
        ordering = self.request.GET.get("ordering")

        if not query:
            return super().list(request, *args, **kwargs)

        # Call Algolia Search API
        algolia_response = AlgoliaService().search(query, page, page_size, ordering)

        # Extract pagination details
        total_results = algolia_response.get("nbHits", 0)
        total_pages = algolia_response.get("nbPages", 1)
        current_page = algolia_response.get("page", 0) + 1  # Convert to 1-based index
        hits = algolia_response.get("hits", [])

        # Compute next & previous page numbers
        next_page = current_page + 1 if current_page < total_pages else None
        prev_page = current_page - 1 if current_page > 1 else None

        # Create a custom pagination response
        return Response({
            "count": total_results,
            "page": current_page,
            "total_pages": total_pages,
            "next": f"?query={query}&page={next_page}&page_size={page_size}" if next_page else None,
            "previous": f"?query={query}&page={prev_page}&page_size={page_size}" if prev_page else None,
            "results": hits,
        })