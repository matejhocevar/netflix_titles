from rest_framework.response import Response

from netflix_titles.views import NetflixTitleViewSet
from .services import ElasticsearchService

class ElasticsearchSearchViewSet(NetflixTitleViewSet):
    """
    Extends NetflixTitleViewSet but modifies search behavior to use Elasticsearch.
    """

    def get_queryset(self):
        """
        Prevents Django ORM queries when Elasticsearch is handling search.
        Returns default queryset when no search query is provided.
        """
        query = self.request.GET.get("search", "").strip()
        if query:
            return self.queryset.none()
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        query = request.GET.get("search", "")
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))
        ordering = self.request.GET.get("ordering")

        if not query:
            return super().list(request, *args, **kwargs)

        results = ElasticsearchService().search(query, page, page_size)
        return Response(results)
