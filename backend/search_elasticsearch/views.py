from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .services import ElasticsearchService

class ElasticsearchSearchViewSet(ViewSet):
    def list(self, request):
        query = request.GET.get("query", "")
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))

        if not query:
            return Response({"error": "Query parameter is required"}, status=400)

        results = ElasticsearchService().search(query, page, page_size)
        return Response(results)
