from django.urls import path
from .views import ElasticsearchSearchViewSet

urlpatterns = [
    path("", ElasticsearchSearchViewSet.as_view({"get": "list"})),
]