from django.shortcuts import render, get_object_or_404
from .models import LearningResource

def resource_detail(request, subject_slug, topic_slug, resource_slug):
    resource = get_object_or_404(LearningResource, topic__subject__slug=subject_slug, topic__slug=topic_slug, slug=resource_slug, status='published')
    related = LearningResource.objects.filter(topic=resource.topic, status='published').exclude(id=resource.id)[:5]
    return render(request, 'learning/detail.html', {'resource': resource, 'related': related, 'subject': resource.topic.subject, 'topic': resource.topic})

def resource_list(request):
    resources = LearningResource.objects.filter(status='published').select_related('topic','topic__subject').order_by('-created_at')[:50]
    return render(request, 'learning/list.html', {'resources': resources})
