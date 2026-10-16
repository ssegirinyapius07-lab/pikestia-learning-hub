from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.bookmarks.models import Bookmark
from apps.core.search import filter_by_terms, with_title_relevance
from apps.subjects.models import Subject, Topic

from .models import LearningResource


PUBLIC_RESOURCE_FILTERS = {
    'status': LearningResource.Status.PUBLISHED,
    'topic__status': Topic.Status.PUBLISHED,
    'topic__subject__status': Subject.Status.PUBLISHED,
}


def resource_detail(request, subject_slug, topic_slug, resource_slug):
    resource = get_object_or_404(
        LearningResource.objects.select_related('topic', 'topic__subject', 'topic__parent'),
        topic__subject__slug=subject_slug,
        topic__slug=topic_slug,
        topic__status=Topic.Status.PUBLISHED,
        topic__subject__status=Subject.Status.PUBLISHED,
        slug=resource_slug,
        status=LearningResource.Status.PUBLISHED,
    )

    # A child topic is not publicly reachable while its parent is unpublished.
    if resource.topic.parent_id and resource.topic.parent.status != Topic.Status.PUBLISHED:
        from django.http import Http404
        raise Http404

    is_bookmarked = (
        request.user.is_authenticated
        and Bookmark.objects.filter(user=request.user, resource=resource).exists()
    )

    related = list(
        LearningResource.objects.filter(**PUBLIC_RESOURCE_FILTERS, topic=resource.topic)
        .exclude(pk=resource.pk)
        .select_related('topic', 'topic__subject', 'topic__parent')
        .order_by('order', 'title')[:5]
    )

    if len(related) < 5:
        if resource.topic.children.filter(status=Topic.Status.PUBLISHED).exists():
            next_topics = resource.topic.children.filter(status=Topic.Status.PUBLISHED)
        else:
            next_topics = Topic.objects.filter(
                subject=resource.topic.subject,
                parent_id=resource.topic.parent_id,
                status=Topic.Status.PUBLISHED,
            ).exclude(pk=resource.topic_id)

        related_ids = [item.pk for item in related]
        more = (
            LearningResource.objects.filter(
                **PUBLIC_RESOURCE_FILTERS,
                topic__in=next_topics,
            )
            .exclude(pk=resource.pk)
            .exclude(pk__in=related_ids)
            .select_related('topic', 'topic__subject', 'topic__parent')
            .order_by('topic__order', 'order', 'title')[:5 - len(related)]
        )
        related.extend(more)

    return render(
        request,
        'learning/detail.html',
        {
            'resource': resource,
            'related': related,
            'subject': resource.topic.subject,
            'topic': resource.topic,
            'is_bookmarked': is_bookmarked,
        },
    )


def resource_list(request):
    query = request.GET.get('q', '').strip()[:100]
    raw_subject_id = request.GET.get('subject', '').strip()
    raw_topic_id = request.GET.get('topic', '').strip()
    subject_id = raw_subject_id if raw_subject_id.isdigit() else ''
    topic_id = raw_topic_id if raw_topic_id.isdigit() else ''

    subjects = Subject.objects.filter(
        status=Subject.Status.PUBLISHED,
    ).order_by('order', 'title')
    selected_subject = subjects.filter(pk=subject_id).first() if subject_id else None

    visible_topics = Topic.objects.filter(
        status=Topic.Status.PUBLISHED,
        subject__status=Subject.Status.PUBLISHED,
    ).filter(
        Q(parent__isnull=True) | Q(parent__status=Topic.Status.PUBLISHED)
    )
    selected_topic = visible_topics.filter(pk=topic_id).first() if topic_id else None

    # Do not let a stale or manually combined URL silently produce confusing
    # empty results for a topic that belongs to a different subject.
    if selected_subject and selected_topic and selected_topic.subject_id != selected_subject.pk:
        topic_id = ''
        selected_topic = None

    resources = (
        LearningResource.objects.filter(**PUBLIC_RESOURCE_FILTERS)
        .filter(Q(topic__parent__isnull=True) | Q(topic__parent__status=Topic.Status.PUBLISHED))
        .select_related('topic', 'topic__subject', 'topic__parent')
    )

    if query:
        resources = filter_by_terms(
            resources,
            query,
            fields=(
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
        )
        resources = with_title_relevance(resources, query)
        resources = resources.order_by(
            '_search_title_rank',
            'topic__subject__order',
            'topic__order',
            'order',
            'title',
        )
    else:
        resources = resources.order_by(
            'topic__subject__order',
            'topic__subject__title',
            'topic__parent__order',
            'topic__order',
            'order',
            'title',
        )

    if subject_id:
        resources = resources.filter(topic__subject_id=int(subject_id))
    if topic_id:
        resources = resources.filter(topic_id=int(topic_id))

    topics = visible_topics.select_related('subject', 'parent').order_by(
        'subject__order',
        'subject__title',
        'parent__order',
        'parent__title',
        'order',
        'title',
    )

    recommendation_base = LearningResource.objects.filter(**PUBLIC_RESOURCE_FILTERS).filter(
        Q(topic__parent__isnull=True) | Q(topic__parent__status=Topic.Status.PUBLISHED)
    ).select_related('topic', 'topic__subject', 'topic__parent')

    recommended_resources = list(
        recommendation_base.filter(is_featured=True).order_by(
            'topic__subject__order', 'topic__parent__order', 'topic__order', 'order', 'title'
        )[:4]
    )
    if not recommended_resources:
        # A useful, honest fallback: start at the beginning of the published
        # curriculum rather than pretending that recent items are personalised.
        recommended_resources = list(
            recommendation_base.order_by(
                'topic__subject__order', 'topic__parent__order', 'topic__order', 'order', 'title'
            )[:4]
        )

    filter_params = {}
    if query:
        filter_params['q'] = query
    if subject_id:
        filter_params['subject'] = subject_id
    if topic_id:
        filter_params['topic'] = topic_id

    paginator = Paginator(resources, 18)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(
        request,
        'learning/list.html',
        {
            'page_obj': page_obj,
            'resources': page_obj.object_list,
            'subjects': subjects,
            'topics': topics,
            'query': query,
            'selected_subject_id': subject_id,
            'selected_topic_id': topic_id,
            'selected_subject': selected_subject,
            'selected_topic': selected_topic,
            'recommended_resources': recommended_resources,
            'has_curated_recommendations': recommendation_base.filter(is_featured=True).exists(),
            'filter_query': urlencode(filter_params),
        },
    )
