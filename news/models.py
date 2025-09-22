from django.db import models
from django.utils import timezone


class Article(models.Model):
    source_id = models.CharField(max_length=255, blank=True)  
    source_name = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True, db_index=True)
    title = models.CharField(max_length=1000, db_index=True)  
    description = models.TextField(blank=True)
    url = models.URLField(unique=True)
    url_to_image = models.URLField(blank=True)
    published_at = models.DateTimeField(default=timezone.now, db_index=True)
    content = models.TextField(blank=True)

    class Meta:
        ordering = ("-published_at",)
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["published_at"]),
        ]

    def __str__(self):
       
        return self.title[:50]
