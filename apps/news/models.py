from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.core.content import sanitize_content
from apps.core.models import EditorialContent


class NewsArticle(EditorialContent):
    class Category(models.TextChoices):
        CAMPUS = 'campus', 'Campus'
        ACADEMIC = 'academic', 'Academic'
        TECHNOLOGY = 'technology', 'Technology'
        CAREER = 'career', 'Career'
        COMMUNITY = 'community', 'Community'
        GENERAL = 'general', 'General'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        REVIEW = 'review', 'In Review'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    summary = models.TextField(blank=True)
    body = models.TextField(help_text='Sanitized HTML')
    body_raw = models.TextField(
        blank=True,
        help_text='Original article HTML before sanitization',
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.GENERAL,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='news_articles',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    published_at = models.DateTimeField(null=True, blank=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['category', '-published_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['featured', '-published_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        raw = self.body_raw or self.body
        self.body = sanitize_content(raw)

        if not self.body_raw:
            self.body_raw = raw

        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED
