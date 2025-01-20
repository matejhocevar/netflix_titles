from django.db import models

from django.db import models

class NetflixTitle(models.Model):
    SHOW_TYPE_CHOICES = [
        ('Movie', 'Movie'),
        ('TV Show', 'TV Show'),
    ]

    show_id = models.CharField(max_length=10, unique=True, primary_key=True)
    type = models.CharField(max_length=10, choices=SHOW_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255, null=True, blank=True)
    cast = models.TextField(null=True, blank=True)  # Store as comma-separated
    country = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateField(null=True, blank=True)
    release_year = models.IntegerField()
    rating = models.CharField(max_length=20, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)  # e.g., "90 min" or "2 Seasons"
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} ({self.release_year})'

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'