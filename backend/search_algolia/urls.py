from django.urls import path
from .views import AlgoliaSearchViewSet

urlpatterns = [
    path("", AlgoliaSearchViewSet.as_view({"get": "list"})),
    path("<str:show_id>/", AlgoliaSearchViewSet.as_view({"get": "retrieve"})),
]