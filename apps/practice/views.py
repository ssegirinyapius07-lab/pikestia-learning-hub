from django.shortcuts import render, get_object_or_404
from .models import PracticeQuestion
from apps.subjects.models import Topic

def practice_by_topic(request, subject_slug, topic_slug):
    topic = get_object_or_404(Topic, subject__slug=subject_slug, slug=topic_slug, status='published')
    questions = topic.questions.filter(status='published')
    return render(request, 'practice/by_topic.html', {'topic': topic, 'questions': questions, 'subject': topic.subject})

def practice_list(request):
    questions = PracticeQuestion.objects.filter(status='published').select_related('topic','topic__subject')[:100]
    return render(request, 'practice/list.html', {'questions': questions})
