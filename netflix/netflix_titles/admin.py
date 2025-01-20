from django.contrib import admin

from .models import NetflixTitle

@admin.register(NetflixTitle)
class NetflixTitleAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('title', 'type', 'release_year', 'rating', 'date_added', 'country')

    # Fields to filter by in the sidebar
    list_filter = ('type', 'release_year', 'rating', 'country')

    # Fields to search by
    search_fields = ('title', 'director', 'cast', 'country', 'description')

    # Field ordering in the admin list view
    ordering = ('-release_year', 'title')

    # Number of items to show per page
    list_per_page = 20
