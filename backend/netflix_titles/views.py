from rest_framework.viewsets import ModelViewSet
from .models import NetflixTitle
from .serializers import NetflixTitleSerializer

class NetflixTitleViewSet(ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting Netflix titles.
    """
    queryset = NetflixTitle.objects.all()
    serializer_class = NetflixTitleSerializer

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