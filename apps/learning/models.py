from django.conf import settings
from django.db import models
from django.utils.text import slugify
import bleach

ALLOWED_TAGS = ['p','h2','h3','h4','ul','ol','li','strong','em','code','pre','blockquote','a','table','thead','tbody','tr','th','td','br','hr','div','span','sup','sub','dl','dt','dd','figure','figcaption','mark']
ALLOWED_PROTOCOLS = {'http', 'https', 'mailto'}
ALLOWED_ATTRS = {
    'a': ['href', 'title', 'rel'],
    'div': ['class'],
    'span': ['class'],
    'mark': ['class'],
}


class LearningResource(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        REVIEW = 'review', 'In Review'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    topic = models.ForeignKey(
        'subjects.Topic',
        on_delete=models.CASCADE,
        related_name='resources',
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=260)
    summary = models.TextField(blank=True)
    objectives = models.TextField(blank=True, help_text="One per line")
    content = models.TextField(help_text="Sanitized HTML")
    content_raw = models.TextField(
        blank=True,
        help_text="Original before sanitization for admin",
    )
    key_concepts = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='learning_resources',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('topic', 'slug')
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        raw = self.content_raw or self.content
        self.content = bleach.clean(
            raw,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=ALLOWED_PROTOCOLS,
            strip=True,
            strip_comments=True,
        )
        if not self.content_raw:
            self.content_raw = raw

        super().save(*args, **kwargs)

    @property
    def objectives_list(self):
        return [item.strip() for item in self.objectives.splitlines() if item.strip()]

    @property
    def key_concepts_list(self):
        return [item.strip() for item in self.key_concepts.split(',') if item.strip()]
