from django.db import models
from django.utils.text import slugify

class Subject(models.Model):
    class Status(models.TextChoices):
        DRAFT='draft','Draft'
        PUBLISHED='published','Published'
        ARCHIVED='archived','Archived'
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField(blank=True)
    discipline = models.CharField(max_length=100, help_text="e.g. Information Technology, Business")
    icon = models.CharField(max_length=50, blank=True, help_text="lucide/icon name")
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order','title']
        indexes = [models.Index(fields=['slug']), models.Index(fields=['discipline']), models.Index(fields=['status'])]

    def __str__(self): return self.title
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args,**kwargs)

class Topic(models.Model):
    class Status(models.TextChoices):
        DRAFT='draft','Draft'
        PUBLISHED='published','Published'
        ARCHIVED='archived','Archived'
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    summary = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('subject','slug')
        ordering = ['order','title']
        indexes = [models.Index(fields=['slug']), models.Index(fields=['status'])]

    def __str__(self): return f"{self.subject.title} - {self.title}"
    def save(self,*args,**kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args,**kwargs)
