from django.shortcuts import render, get_object_or_404
from .models import Subject, Topic

def subject_list(request):
    subjects = Subject.objects.filter(status='published').prefetch_related('topics')
    return render(request, 'subjects/list.html', {'subjects': subjects})

def subject_detail(request, slug):
    subject = get_object_or_404(Subject, slug=slug, status='published')
    topics = subject.topics.filter(status='published').order_by('order')
    return render(request, 'subjects/detail.html', {'subject': subject, 'topics': topics})

def topic_detail(request, subject_slug, topic_slug):
    subject = get_object_or_404(Subject, slug=subject_slug, status='published')
    topic = get_object_or_404(Topic, subject=subject, slug=topic_slug, status='published')
    resources = topic.resources.filter(status='published').order_by('order')
    related = Topic.objects.filter(subject=subject, status='published').exclude(id=topic.id)[:5]
    return render(request, 'subjects/topic.html', {'subject': subject, 'topic': topic, 'resources': resources, 'related': related})
