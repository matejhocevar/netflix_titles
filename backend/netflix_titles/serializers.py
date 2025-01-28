from rest_framework import serializers
from .models import NetflixTitle

class NetflixTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetflixTitle
        fields = [
            "show_id",
            "title",
            "type",
            "director",
            "duration",
            "country",
            "release_year",
            "description",
            "rating",
            "date_added",
        ]