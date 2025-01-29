from django.urls import path
from .views import ElasticsearchSearchViewSet

urlpatterns = [
    path("search/elasticsearch/", ElasticsearchSearchViewSet.as_view({"get": "list"})),
]