from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Opportunity(models.Model):
    class Category(models.TextChoices):
        SCHOLARSHIP='scholarship','Scholarship'
        INTERNSHIP='internship','Internship'
        COMPETITION='competition','Competition'
        HACKATHON='hackathon','Hackathon'
        WORKSHOP='workshop','Workshop'
        TRAINING='training','Training'
        OTHER='other','Other'
    class Status(models.TextChoices):
        DRAFT='draft','Draft'
        ACTIVE='active','Active'
        EXPIRED='expired','Expired'
        ARCHIVED='archived','Archived'

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=260)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices)
    eligibility = models.TextField(blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_remote = models.BooleanField(default=False)
    source_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_verified = models.BooleanField(default=False)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Opportunity'
        verbose_name_plural = 'Opportunities'
        ordering=['-published_at']
        indexes=[models.Index(fields=['status']), models.Index(fields=['category']), models.Index(fields=['deadline'])]

    def __str__(self): return self.title
    def save(self,*args,**kwargs):
        if not self.slug: self.slug = slugify(self.title)
        # auto-expire
        if self.deadline and self.deadline < timezone.now() and self.status == self.Status.ACTIVE:
            self.status = self.Status.EXPIRED
        super().save(*args,**kwargs)

    @property
    def is_expired(self):
        return self.deadline and self.deadline < timezone.now()
