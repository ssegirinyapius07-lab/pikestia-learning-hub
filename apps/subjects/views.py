from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Subject, Topic


def _with_public_counts(queryset):
    return queryset.annotate(
        resource_count=Count(
            'resources',
            filter=Q(resources__status='published'),
            distinct=True,
        ),
        question_count=Count(
            'questions',
            filter=Q(questions__status='published'),
            distinct=True,
        ),
    )


def subject_list(request):
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
    return render(request, 'subjects/list.html', {'subjects': subjects})


def subject_detail(request, slug):
    subject = get_object_or_404(
        Subject,
        slug=slug,
        status=Subject.Status.PUBLISHED,
    )
    topics = _with_public_counts(
        subject.topics.filter(
            status=Topic.Status.PUBLISHED,
            parent__isnull=True,
        )
    ).order_by('order', 'title')

    return render(
        request,
        'subjects/detail.html',
        {'subject': subject, 'topics': topics},
    )


def topic_detail(request, subject_slug, topic_slug):
    topic = get_object_or_404(
        _with_public_counts(
            Topic.objects.filter(
                subject__slug=subject_slug,
                subject__status=Subject.Status.PUBLISHED,
                status=Topic.Status.PUBLISHED,
            ).filter(
                Q(parent__isnull=True) | Q(parent__status=Topic.Status.PUBLISHED)
            )
        ).select_related('subject', 'parent'),
        slug=topic_slug,
    )
    subject = topic.subject

    children = _with_public_counts(
        topic.children.filter(status=Topic.Status.PUBLISHED)
    ).order_by('order', 'title')

    resources = topic.resources.filter(
        status='published',
    ).order_by('order', 'title')

    related = (
        Topic.objects.filter(
            subject=subject,
            parent_id=topic.parent_id,
            status=Topic.Status.PUBLISHED,
        )
        .exclude(pk=topic.pk)
        .order_by('order', 'title')[:5]
    )

    return render(
        request,
        'subjects/topic.html',
        {
            'subject': subject,
            'topic': topic,
            'children': children,
            'resources': resources,
            'related': related,
        },
    )
