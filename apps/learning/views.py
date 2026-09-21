from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.subjects.models import Subject, Topic

from .models import LearningResource


def resource_detail(request, subject_slug, topic_slug, resource_slug):
    resource = get_object_or_404(
        LearningResource.objects.select_related('topic', 'topic__subject'),
        topic__subject__slug=subject_slug,
        topic__slug=topic_slug,
        slug=resource_slug,
        status='published',
    )
    related = (
        LearningResource.objects.filter(topic=resource.topic, status='published')
        .exclude(id=resource.id)
        .order_by('order', 'title')[:5]
    )
    return render(
        request,
        'learning/detail.html',
        {
            'resource': resource,
            'related': related,
            'subject': resource.topic.subject,
            'topic': resource.topic,
        },
    )


def resource_list(request):
    query = request.GET.get('q', '').strip()[:100]
    subject_id = request.GET.get('subject', '').strip()
    topic_id = request.GET.get('topic', '').strip()

    resources = (
        LearningResource.objects.filter(status=LearningResource.Status.PUBLISHED)
        .select_related('topic', 'topic__subject')
        .order_by(
            'topic__subject__title',
            'topic__order',
            'order',
            'title',
        )
    )

    if query:
        resources = resources.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(key_concepts__icontains=query)
            | Q(topic__title__icontains=query)
            | Q(topic__subject__title__icontains=query)
        )

    if subject_id.isdigit():
        resources = resources.filter(topic__subject_id=int(subject_id))

    if topic_id.isdigit():
        resources = resources.filter(topic_id=int(topic_id))

    subjects = Subject.objects.filter(
        status=Subject.Status.PUBLISHED
    ).order_by('order', 'title')

    topics = Topic.objects.filter(
        status=Topic.Status.PUBLISHED
    ).select_related('subject').order_by('subject__order', 'subject__title', 'order', 'title')

    filter_params = {}
    if query:
        filter_params['q'] = query
    if subject_id.isdigit():
        filter_params['subject'] = subject_id
    if topic_id.isdigit():
        filter_params['topic'] = topic_id

    paginator = Paginator(resources, 18)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    filter_query = urlencode(filter_params)

    return render(
        request,
        'learning/list.html',
        {
            'page_obj': page_obj,
            'resources': page_obj.object_list,
            'subjects': subjects,
            'topics': topics,
            'query': query,
            'selected_subject_id': subject_id if subject_id.isdigit() else '',
            'selected_topic_id': topic_id if topic_id.isdigit() else '',
            'filter_query': filter_query,
        },
    )
