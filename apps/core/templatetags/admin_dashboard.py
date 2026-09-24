from django import template
from apps.accounts.models import AuditLog, User
from apps.learning.models import LearningResource
from apps.news.models import NewsArticle
from apps.opportunities.models import Opportunity
from apps.practice.models import PracticeQuestion
from apps.subjects.models import Subject

register = template.Library()


@register.simple_tag
def admin_dashboard_summary():
    return {
        'users': User.objects.count(),
        'learning': LearningResource.objects.count(),
        'news': NewsArticle.objects.count(),
        'subjects': Subject.objects.count(),
        'practice': PracticeQuestion.objects.count(),
        'opportunities': Opportunity.objects.count(),
        'published_learning': LearningResource.objects.filter(
            status=LearningResource.Status.PUBLISHED
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
        'recent_activity': AuditLog.objects.select_related('user').order_by(
            '-created_at'
        )[:6],
    }
