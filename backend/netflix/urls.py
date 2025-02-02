from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from netflix_titles.views import NetflixTitleViewSet

router = DefaultRouter()
# router.register(r'titles', NetflixTitleViewSet, basename='title')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/django/', include("netflix_titles.urls")),
    path("api/elasticsearch/", include("search_elasticsearch.urls")),
    path("api/algolia/", include("search_algolia.urls")),
]
