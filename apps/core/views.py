from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from apps.subjects.models import Subject
from apps.learning.models import LearningResource
from apps.opportunities.models import Opportunity
from apps.accounts.models import CookiePreference
from apps.news.models import NewsArticle


def home_view(request):
    subjects = Subject.objects.filter(status='published').order_by('order')[:8]

    featured = (
        LearningResource.objects.filter(status='published')
        .select_related('topic', 'topic__subject')
        .order_by('-created_at')[:6]
    )

    now = timezone.now()
    opportunities = (
        Opportunity.objects.filter(status='active')
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
    subjects = Subject.objects.filter(status='published')
    return render(request, 'core/explore.html', {'subjects': subjects})


@ratelimit(key='ip', rate='30/m', block=True)
def search_view(request):
    q = request.GET.get('q', '').strip()[:100]
    results = {'subjects': [], 'topics': [], 'resources': [], 'opportunities': [], 'news': []}
    if q:
        from apps.subjects.models import Subject, Topic
        from apps.learning.models import LearningResource
        from apps.opportunities.models import Opportunity

        results['subjects'] = Subject.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q),
            status='published',
        )[:10]
        results['topics'] = Topic.objects.filter(
            Q(title__icontains=q) | Q(summary__icontains=q),
            status='published',
        ).select_related('subject')[:10]
        results['resources'] = LearningResource.objects.filter(
            Q(title__icontains=q) | Q(summary__icontains=q),
            status='published',
        )[:10]
        now = timezone.now()
        results['opportunities'] = Opportunity.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q),
            status='active',
        ).filter(
            Q(deadline__isnull=True) | Q(deadline__gt=now)
        )[:10]
        results['news'] = NewsArticle.objects.filter(
            Q(title__icontains=q)
            | Q(summary__icontains=q)
            | Q(body__icontains=q)
            | Q(author__full_name__icontains=q),
            status=NewsArticle.Status.PUBLISHED,
        ).select_related('author').order_by('-published_at')[:10]
    return render(request, 'core/search.html', {'query': q, 'results': results})


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
        from django.utils import timezone
        request.user.last_theme_sync = timezone.now()
        request.user.save(update_fields=['display_mode', 'last_theme_sync'])
    request.session['display_mode'] = mode
    resp = redirect(request.META.get('HTTP_REFERER', '/'))
    resp.set_cookie(
        'display_mode',
        mode,
        max_age=60 * 60 * 24 * 365,
        samesite='Lax',
        secure=False,
        httponly=False,
    )
    return resp


@require_http_methods(["POST"])
def set_cookie_consent_view(request):
    choice = request.POST.get('choice')
    analytics = choice == 'all' or request.POST.get('analytics') == 'on'
    marketing = choice == 'all' or request.POST.get('marketing') == 'on'
    if choice == 'reject':
        analytics = False
        marketing = False

    if request.user.is_authenticated:
        pref, _ = CookiePreference.objects.get_or_create(user=request.user)
        pref.analytics = analytics
        pref.marketing = marketing
        pref.save()
    else:
        session_key = request.session.session_key or ''
        pref, _ = CookiePreference.objects.get_or_create(session_key=session_key, user=None)
        pref.analytics = analytics
        pref.marketing = marketing
        pref.save()

    resp = redirect(request.META.get('HTTP_REFERER', '/'))
    import json
    resp.set_cookie(
        'cookie_consent',
        json.dumps({'analytics': analytics, 'marketing': marketing}),
        max_age=60 * 60 * 24 * 365,
        samesite='Lax',
    )
    return resp


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
