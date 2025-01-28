from rest_framework import serializers
from .models import NetflixTitle

class NetflixTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetflixTitle
        fields = [
            "show_id",
            "title",
            "type",
            "release_year",
            "rating",
            "country",
            "date_added",
            "description",
        ]