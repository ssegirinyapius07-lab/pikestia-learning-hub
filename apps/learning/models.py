from django.db import models
from django.utils.text import slugify
import bleach

ALLOWED_TAGS = [
    'p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'strong', 'em', 'code',
    'pre', 'blockquote', 'a', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'br', 'hr', 'div', 'span', 'sup', 'sub', 'dl', 'dt', 'dd', 'figure',
    'figcaption', 'mark', 'img',
]
ALLOWED_PROTOCOLS = {'http', 'https', 'mailto'}
ALLOWED_ATTRS = {
    'a': ['href', 'title', 'rel'],
    'div': ['class'],
    'span': ['class'],
    'mark': ['class'],
    'img': ['src', 'alt', 'title', 'width', 'height', 'loading'],
}


class LearningResource(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    topic = models.ForeignKey('subjects.Topic', on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=260)
    summary = models.TextField(blank=True)
    objectives = models.TextField(blank=True, help_text='One per line')
    content = models.TextField(help_text='Sanitized HTML')
    content_raw = models.TextField(blank=True, help_text='Original before sanitization for admin')
    key_concepts = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(
        default=False,
        help_text='Feature this published material in Pikestia recommendations and the homepage.',
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('topic', 'slug')
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_featured', 'status'], name='lr_featured_status_idx'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        raw = self.content_raw or self.content
        cleaned = bleach.clean(
            raw,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=ALLOWED_PROTOCOLS,
            strip=True,
            strip_comments=True,
        )
        self.content = cleaned
        if not self.content_raw:
            self.content_raw = raw
        super().save(*args, **kwargs)

    @property
    def objectives_list(self):
        return [objective.strip() for objective in self.objectives.splitlines() if objective.strip()]

    @property
    def key_concepts_list(self):
        return [concept.strip() for concept in self.key_concepts.split(',') if concept.strip()]
