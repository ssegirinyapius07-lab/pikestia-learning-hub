from django.db import models
from django.db.models import Q
from django.conf import settings


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
    )
    resource = models.ForeignKey(
        'learning.LearningResource',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    topic = models.ForeignKey(
        'subjects.Topic',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    opportunity = models.ForeignKey(
        'opportunities.Opportunity',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user'])]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(resource__isnull=False, topic__isnull=True, opportunity__isnull=True)
                    | Q(resource__isnull=True, topic__isnull=False, opportunity__isnull=True)
                    | Q(resource__isnull=True, topic__isnull=True, opportunity__isnull=False)
                ),
                name='bookmark_exactly_one_target',
            ),
            models.UniqueConstraint(
                fields=['user', 'resource'],
                condition=Q(resource__isnull=False),
                name='unique_user_resource_bookmark',
            ),
            models.UniqueConstraint(
                fields=['user', 'topic'],
                condition=Q(topic__isnull=False),
                name='unique_user_topic_bookmark',
            ),
            models.UniqueConstraint(
                fields=['user', 'opportunity'],
                condition=Q(opportunity__isnull=False),
                name='unique_user_opportunity_bookmark',
            ),
        ]

    def __str__(self):
        return f"{self.user.email} - bookmark"
