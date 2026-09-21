from django.db import models
from django.conf import settings

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    resource = models.ForeignKey('learning.LearningResource', null=True, blank=True, on_delete=models.CASCADE)
    topic = models.ForeignKey('subjects.Topic', null=True, blank=True, on_delete=models.CASCADE)
    opportunity = models.ForeignKey('opportunities.Opportunity', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']
        indexes=[models.Index(fields=['user'])]

    def __str__(self):
        return f"{self.user.email} - bookmark"
