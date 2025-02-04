from django.urls import path
from .views import NetflixTitleViewSet, NetflixFiltersView

urlpatterns = [
    path("", NetflixTitleViewSet.as_view({"get": "list"})),
    path("filters/", NetflixFiltersView.as_view()),
    path("<str:show_id>/", NetflixTitleViewSet.as_view({"get": "retrieve"})),
]