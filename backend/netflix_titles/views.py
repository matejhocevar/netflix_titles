from django.db.models import Q
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
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
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = [
        'title',
        'director',
        'description',
        'release_year',
        'country',
    ]
    ordering_fields = [
        'title',
        'type',
        'director',
        'duration',
        'country',
        'release_year',
    ]
    ordering = ['title']
    lookup_field = 'show_id'

    def get_queryset(self):
        """
        Apply multiple filters dynamically based on query parameters.
        """
        queryset = super().get_queryset()
        request = self.request

        # Free-text search
        search_query = request.GET.get("search", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(director__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(country__icontains=search_query)
            )

        # Filters: Multiple values (CSV format)
        type_filter = request.GET.get("type")
        country_filter = request.GET.get("country")
        rating_filter = request.GET.get("rating")

        if type_filter:
            types = type_filter.split(",")  # Split CSV values
            queryset = queryset.filter(type__in=types)

        if country_filter:
            countries = country_filter.split(",")
            queryset = queryset.filter(country__in=countries)

        if rating_filter:
            ratings = rating_filter.split(",")
            queryset = queryset.filter(rating__in=ratings)

        # Filters: Numeric Ranges
        release_year_min = request.GET.get("release_year_gte")
        release_year_max = request.GET.get("release_year_lte")

        if release_year_min:
            queryset = queryset.filter(release_year__gte=int(release_year_min))
        if release_year_max:
            queryset = queryset.filter(release_year__lte=int(release_year_max))

        # Duration filter
        duration_filter = request.GET.get("duration")
        if duration_filter:
            if duration_filter == "short":
                # Filter for durations less than 60 min
                queryset = queryset.filter(duration__regex=r"^\b([1-5]?[0-9]) min\b$")
            elif duration_filter == "medium":
                # Filter for durations between 60 and 120 min
                queryset = queryset.filter(duration__regex=r"^\b(6[0-9]|[7-9][0-9]|1[0-1][0-9]|120) min\b$")
            elif duration_filter == "long":
                # Filter for durations greater than 120 min
                queryset = queryset.filter(duration__regex=r"^\b(12[1-9]|[2-9][0-9][0-9]|[1-9][0-9]{2,}) min\b$")
            elif "Season" in duration_filter:
                if duration_filter == "5/ Seasons":
                    queryset = queryset.filter(duration__regex=r"^\b([5-9]|[1-9][0-9]) Seasons?\b$")
                else:
                    queryset = queryset.filter(duration__iexact=duration_filter)

        return queryset

class NetflixFiltersView(APIView):
    """
    API endpoint to return available filter options dynamically.
    """
    def get(self, request, *args, **kwargs):
        countries = (
            NetflixTitle.objects.exclude(country__isnull=True)
            .exclude(country="")
            .values_list("country", flat=True)
            .distinct()
        )

        ratings = (
            NetflixTitle.objects.exclude(rating__isnull=True)
            .exclude(rating="")
            .values_list("rating", flat=True)
            .distinct()
        )

        types = (
            NetflixTitle.objects.values_list("type", flat=True)
            .distinct()
        )

        return Response(
            {
                "countries": sorted(list(countries)),
                "ratings": sorted(list(ratings)),
                "types": sorted(list(types)),
            },
            status=status.HTTP_200_OK,
        )