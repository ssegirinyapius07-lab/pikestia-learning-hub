from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EditorialContent(TimeStampedModel):
    title = models.CharField(max_length=250)

    class Meta:
        abstract = True
