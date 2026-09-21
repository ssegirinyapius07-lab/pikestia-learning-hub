from django.db import models


class EditorialContent(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
