from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .models import NetflixTitle
from .serializers import NetflixTitleSerializer


class NetflixTitlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class NetflixTitleViewSet(ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting Netflix titles.
    """
    queryset = NetflixTitle.objects.all()
    serializer_class = NetflixTitleSerializer
    pagination_class = NetflixTitlePagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'title',
        'director',
        'description',
        'release_year',
        'country',
    ]
    ordering_fields = [
        'show_id',
        'title',
        'type',
        'director',
        'duration',
        'country',
        'release_year',
        'rating',
        'date_added',
    ]
    ordering = ['title']

    def get_queryset(self):
        """
        Optionally filter the queryset by 'title' or 'type' query params.
        """
        queryset = super().get_queryset()
        title = self.request.GET.get("title")
        type_filter = self.request.GET.get("type")
        if title:
            queryset = queryset.filter(title__icontains=title)
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        return queryset