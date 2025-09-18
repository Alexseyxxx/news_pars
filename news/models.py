from django.db import models

class Article(models.Model):
    source_id = models.CharField(max_length=255, null=True, blank=True)
    source_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(unique=True)
    url_to_image = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField(null=True, blank=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-published_at",)

    def __str__(self):
        return self.title
