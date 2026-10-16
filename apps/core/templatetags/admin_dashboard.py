from django import template
from django.db.models import Count, Q

from apps.accounts.models import AuditLog, User
from apps.learning.models import LearningResource
from apps.news.models import NewsArticle
from apps.opportunities.models import Opportunity
from apps.practice.models import PracticeQuestion
from apps.subjects.models import Subject, Topic

register = template.Library()


@register.simple_tag
def admin_dashboard_summary():
    published_subjects = Subject.objects.filter(status=Subject.Status.PUBLISHED)
    subjects_without_topics = (
        published_subjects.annotate(
            root_topic_count=Count(
                'topics',
                filter=Q(
                    topics__status=Topic.Status.PUBLISHED,
                    topics__parent__isnull=True,
                ),
                distinct=True,
            )
        )
        .filter(root_topic_count=0)
        .count()
    )

    visible_topics = Topic.objects.filter(
        status=Topic.Status.PUBLISHED,
        subject__status=Subject.Status.PUBLISHED,
    ).filter(
        Q(parent__isnull=True) | Q(parent__status=Topic.Status.PUBLISHED)
    )
    topics_without_learning = (
        visible_topics.annotate(
            published_resource_count=Count(
                'resources',
                filter=Q(resources__status=LearningResource.Status.PUBLISHED),
                distinct=True,
            ),
            published_child_count=Count(
                'children',
                filter=Q(children__status=Topic.Status.PUBLISHED),
                distinct=True,
            ),
        )
        .filter(published_resource_count=0, published_child_count=0)
        .count()
    )

    published_resources = LearningResource.objects.filter(
        status=LearningResource.Status.PUBLISHED,
    )
    resources_needing_editorial_review = published_resources.filter(
        Q(summary='') | Q(objectives='') | Q(key_concepts='')
    ).count()

    return {
        'users': User.objects.count(),
        'learning': LearningResource.objects.count(),
        'news': NewsArticle.objects.count(),
        'subjects': Subject.objects.count(),
        'practice': PracticeQuestion.objects.count(),
        'opportunities': Opportunity.objects.count(),
        'published_learning': published_resources.count(),
        'featured_learning': published_resources.filter(is_featured=True).count(),
        'draft_learning': LearningResource.objects.filter(
            status=LearningResource.Status.DRAFT
        ).count(),
        'published_news': NewsArticle.objects.filter(
            status=NewsArticle.Status.PUBLISHED
        ).count(),
        'review_news': NewsArticle.objects.filter(
            status=NewsArticle.Status.REVIEW
        ).count(),
        'active_opportunities': Opportunity.objects.filter(
            status=Opportunity.Status.ACTIVE
        ).count(),
        'published_subjects_without_topics': subjects_without_topics,
        'published_topics_without_learning': topics_without_learning,
        'resources_needing_editorial_review': resources_needing_editorial_review,
        'recent_activity': AuditLog.objects.select_related('user').order_by(
            '-created_at'
        )[:6],
    }
