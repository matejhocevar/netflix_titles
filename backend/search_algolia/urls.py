from django.urls import path
from .views import AlgoliaSearchViewSet

urlpatterns = [
    path("search/algolia/", AlgoliaSearchViewSet.as_view({"get": "list"})),
    path("search/algolia/<str:show_id>/", AlgoliaSearchViewSet.as_view({"get": "retrieve"})),
]