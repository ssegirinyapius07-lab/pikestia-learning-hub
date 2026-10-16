from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Subject(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField(blank=True)
    discipline = models.CharField(
        max_length=100,
        help_text='Academic group or branch, e.g. Science & Technology or Business.',
    )
    icon = models.CharField(max_length=50, blank=True, help_text='lucide/icon name')
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['discipline']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Topic(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        help_text='Optional parent topic. Use this to group lessons, for example Web Design → HTML Fundamentals.',
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    summary = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('subject', 'slug')
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['parent', 'order'], name='subjects_to_parent_order_idx'),
        ]

    def __str__(self):
        if self.parent_id:
            return f'{self.subject.title} - {self.parent.title} - {self.title}'
        return f'{self.subject.title} - {self.title}'

    def clean(self):
        super().clean()
        errors = {}

        if not self.parent_id:
            return

        if self.pk and self.parent_id == self.pk:
            errors['parent'] = 'A topic cannot be its own parent.'
        elif self.parent.subject_id != self.subject_id:
            errors['parent'] = 'Parent and child topics must belong to the same subject.'
        elif self.parent.parent_id:
            errors['parent'] = 'Choose a top-level topic as the parent. Pikestia supports one subgroup level beneath a topic.'

        if self.pk and self.children.exists():
            errors['parent'] = 'This topic already contains subtopics and cannot be moved beneath another topic.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
