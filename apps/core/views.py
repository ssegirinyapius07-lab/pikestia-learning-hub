from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from apps.accounts.models import CookiePreference
from apps.core.search import filter_by_terms, with_title_relevance
from apps.learning.models import LearningResource
from apps.news.models import NewsArticle
from apps.opportunities.models import Opportunity
from apps.practice.models import PracticeQuestion
from apps.subjects.models import Subject, Topic


def _public_resources():
    return LearningResource.objects.filter(
        status=LearningResource.Status.PUBLISHED,
        topic__status=Topic.Status.PUBLISHED,
        topic__subject__status=Subject.Status.PUBLISHED,
    ).filter(
        Q(topic__parent__isnull=True) | Q(topic__parent__status=Topic.Status.PUBLISHED)
    ).select_related('topic', 'topic__subject', 'topic__parent')


def _starting_resources(limit=4):
    """Return editor-selected resources, or an orderly curriculum-based fallback."""
    resources = _public_resources()
    featured = list(
        resources.filter(is_featured=True).order_by(
            'topic__subject__order',
            'topic__parent__order',
            'topic__order',
            'order',
            'title',
        )[:limit]
    )
    if featured:
        return featured

    return list(
        resources.order_by(
            'topic__subject__order',
            'topic__parent__order',
            'topic__order',
            'order',
            'title',
        )[:limit]
    )


def home_view(request):
    subjects = (
        Subject.objects.filter(status=Subject.Status.PUBLISHED)
        .annotate(
            topic_count=Count(
                'topics',
                filter=Q(
                    topics__status=Topic.Status.PUBLISHED,
                    topics__parent__isnull=True,
                ),
                distinct=True,
            )
        )
        .order_by('order', 'title')[:8]
    )

    featured = _public_resources().order_by(
        '-is_featured',
        'topic__subject__order',
        'topic__subject__title',
        'topic__parent__order',
        'topic__order',
        'order',
        'title',
    )[:6]

    now = timezone.now()
    opportunities = (
        Opportunity.objects.filter(status=Opportunity.Status.ACTIVE)
        .filter(Q(deadline__isnull=True) | Q(deadline__gt=now))
        .order_by('-published_at')[:4]
    )

    published_news = (
        NewsArticle.objects.filter(status=NewsArticle.Status.PUBLISHED)
        .select_related('author')
        .order_by('-published_at', '-created_at')
    )

    latest_news = list(published_news[:6])
    lead_news = (
        published_news.filter(featured=True).first()
        or (latest_news[0] if latest_news else None)
    )
    secondary_news = [
        article for article in latest_news
        if not lead_news or article.pk != lead_news.pk
    ][:2]
    latest_stories = [
        article for article in latest_news
        if not lead_news or article.pk != lead_news.pk
    ]
    latest_stories = [
        article for article in latest_stories
        if article.pk not in {item.pk for item in secondary_news}
    ][:3]

    return render(
        request,
        'core/home.html',
        {
            'subjects': subjects,
            'featured': featured,
            'opportunities': opportunities,
            'latest_news': latest_stories,
            'lead_news': lead_news,
            'secondary_news': secondary_news,
        },
    )


def explore_view(request):
    subjects = (
        Subject.objects.filter(status=Subject.Status.PUBLISHED)
        .annotate(
            topic_count=Count(
                'topics',
                filter=Q(
                    topics__status=Topic.Status.PUBLISHED,
                    topics__parent__isnull=True,
                ),
                distinct=True,
            )
        )
        .order_by('order', 'title')
    )
    return render(request, 'core/explore.html', {'subjects': subjects})


@ratelimit(key='ip', rate='30/m', block=True)
def search_view(request):
    query = request.GET.get('q', '').strip()[:100]
    results = {
        'subjects': [],
        'topics': [],
        'resources': [],
        'practice': [],
        'opportunities': [],
        'news': [],
    }

    if query:
        subjects = Subject.objects.filter(status=Subject.Status.PUBLISHED)
        results['subjects'] = with_title_relevance(
            filter_by_terms(subjects, query, ('title', 'description', 'discipline')),
            query,
        ).order_by('_search_title_rank', 'order', 'title')[:15]

        visible_topics = Topic.objects.filter(
            status=Topic.Status.PUBLISHED,
            subject__status=Subject.Status.PUBLISHED,
        ).filter(
            Q(parent__isnull=True) | Q(parent__status=Topic.Status.PUBLISHED)
        )
        results['topics'] = with_title_relevance(
            filter_by_terms(
                visible_topics,
                query,
                (
                    'title',
                    'summary',
                    'learning_objectives',
                    'subject__title',
                    'subject__discipline',
                    'parent__title',
                ),
            ),
            query,
        ).select_related(
            'subject', 'parent'
        ).order_by(
            '_search_title_rank',
            'subject__order',
            'subject__title',
            'parent__order',
            'order',
            'title',
        )[:15]

        results['resources'] = with_title_relevance(
            filter_by_terms(
                _public_resources(),
                query,
                (
                    'title',
                    'summary',
                    'objectives',
                    'key_concepts',
                    'content',
                    'topic__title',
                    'topic__summary',
                    'topic__learning_objectives',
                    'topic__parent__title',
                    'topic__subject__title',
                    'topic__subject__discipline',
                ),
            ),
            query,
        ).order_by(
            '_search_title_rank',
            'topic__subject__order',
            'topic__parent__order',
            'topic__order',
            'order',
            'title',
        )[:15]

        practice_questions = PracticeQuestion.objects.filter(
            status=PracticeQuestion.Status.PUBLISHED,
            topic__status=Topic.Status.PUBLISHED,
            topic__subject__status=Subject.Status.PUBLISHED,
        ).filter(
            Q(topic__parent__isnull=True) | Q(topic__parent__status=Topic.Status.PUBLISHED)
        )
        results['practice'] = with_title_relevance(
            filter_by_terms(
                practice_questions,
                query,
                (
                    'question',
                    'topic__title',
                    'topic__summary',
                    'topic__parent__title',
                    'topic__subject__title',
                    'topic__subject__discipline',
                ),
            ),
            query,
            title_field='question',
        ).select_related(
            'topic', 'topic__subject', 'topic__parent'
        ).order_by(
            '_search_title_rank',
            'topic__subject__order',
            'topic__parent__order',
            'topic__order',
            'id',
        )[:15]

        now = timezone.now()
        opportunities = Opportunity.objects.filter(
            status=Opportunity.Status.ACTIVE,
        ).filter(
            Q(deadline__isnull=True) | Q(deadline__gt=now)
        )
        results['opportunities'] = with_title_relevance(
            filter_by_terms(
                opportunities,
                query,
                (
                    'title',
                    'description',
                    'eligibility',
                    'location',
                    'source_name',
                    'category',
                ),
            ),
            query,
        ).order_by('_search_title_rank', '-published_at', 'title')[:15]

        articles = NewsArticle.objects.filter(status=NewsArticle.Status.PUBLISHED)
        results['news'] = with_title_relevance(
            filter_by_terms(
                articles,
                query,
                (
                    'title',
                    'summary',
                    'body',
                    'category',
                    'author__full_name',
                ),
            ),
            query,
        ).select_related('author').order_by(
            '_search_title_rank',
            '-published_at',
            '-created_at',
        )[:15]

    result_count = sum(len(items) for items in results.values())
    has_results = result_count > 0

    return render(
        request,
        'core/search.html',
        {
            'query': query,
            'results': results,
            'result_count': result_count,
            'has_results': has_results,
            'recommended_resources': [] if has_results else _starting_resources(),
            'recommended_subjects': (
                Subject.objects.filter(status=Subject.Status.PUBLISHED)
                .order_by('order', 'title')[:4]
                if not has_results else []
            ),
        },
    )


def about_view(request):
    return render(request, 'core/about.html')


@ratelimit(key='ip', rate='5/m', block=True)
@require_http_methods(["GET", "POST"])
def contact_view(request):
    if request.method == "POST":
        name = " ".join(request.POST.get("name", "").split())[:100]
        email = request.POST.get("email", "").strip()[:254]
        message = request.POST.get("message", "").strip()[:5000]

        if not name or not email or not message:
            messages.error(request, "Please complete all contact fields.")
            return render(request, "core/contact.html")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(request, "core/contact.html")

        subject = f"Pikestia Contact Form — Message from {name}"
        body = (
            f"Name: {name}\n"
            f"Email: {email}\n\n"
            "Message:\n"
            f"{message}\n\n"
            f"Submitted from: {request.build_absolute_uri('/contact/')}"
        )

        email_message = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[email],
        )
        email_message.send(fail_silently=False)

        messages.success(
            request,
            "Your message has been sent successfully. We will get back to you as soon as possible.",
        )
        return redirect("contact")

    return render(request, "core/contact.html")


def privacy_view(request):
    return render(request, 'core/legal/privacy.html')


def cookie_policy_view(request):
    return render(request, 'core/legal/cookies.html')


def terms_view(request):
    return render(request, 'core/legal/terms.html')


def acceptable_use_view(request):
    return render(request, 'core/legal/acceptable_use.html')


def copyright_view(request):
    return render(request, 'core/legal/copyright.html')


@require_http_methods(["POST"])
def set_theme_view(request):
    mode = request.POST.get('display_mode')
    if mode not in ('light', 'dark', 'system'):
        return redirect('/')
    if request.user.is_authenticated:
        request.user.display_mode = mode
        request.user.last_theme_sync = timezone.now()
        request.user.save(update_fields=['display_mode', 'last_theme_sync'])
    request.session['display_mode'] = mode
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(
        'display_mode',
        mode,
        max_age=60 * 60 * 24 * 365,
        samesite='Lax',
        secure=not settings.DEBUG,
        httponly=False,
    )
    return response


@require_http_methods(["POST"])
def set_cookie_consent_view(request):
    choice = request.POST.get('choice')
    analytics = choice == 'all' or request.POST.get('analytics') == 'on'
    marketing = choice == 'all' or request.POST.get('marketing') == 'on'
    if choice == 'reject':
        analytics = False
        marketing = False

    if request.user.is_authenticated:
        preference, _ = CookiePreference.objects.get_or_create(user=request.user)
        preference.analytics = analytics
        preference.marketing = marketing
        preference.save()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        preference, _ = CookiePreference.objects.get_or_create(
            session_key=session_key,
            user=None,
        )
        preference.analytics = analytics
        preference.marketing = marketing
        preference.save()

    response = redirect(request.META.get('HTTP_REFERER', '/'))
    import json
    response.set_cookie(
        'cookie_consent',
        json.dumps({'analytics': analytics, 'marketing': marketing}),
        max_age=60 * 60 * 24 * 365,
        samesite='Lax',
        secure=not settings.DEBUG,
    )
    return response


def error_400(request, exception=None):
    return render(request, 'errors/400.html', status=400)


def error_401(request, exception=None):
    return render(request, 'errors/401.html', status=401)


def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)


def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def error_429(request, exception=None):
    return render(request, 'errors/429.html', status=429)


def error_500(request):
    return render(request, 'errors/500.html', status=500)
