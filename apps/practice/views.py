from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.subjects.models import Topic

from .models import PracticeQuestion


def _normalise_answer(value):
    return ' '.join((value or '').strip().lower().split())


def practice_by_topic(request, subject_slug, topic_slug):
    topic = get_object_or_404(
        Topic.objects.select_related('subject'),
        subject__slug=subject_slug,
        slug=topic_slug,
        status=Topic.Status.PUBLISHED,
    )
    questions = list(
        topic.questions.filter(status=PracticeQuestion.Status.PUBLISHED)
        .order_by('id')
    )

    submitted = request.method == 'POST'
    results = []
    score = 0
    graded_count = 0

    if submitted:
        for question in questions:
            answer = request.POST.get(f'question_{question.id}', '').strip()
            is_correct = None

            if question.type in (PracticeQuestion.QType.MCQ, PracticeQuestion.QType.SHORT):
                is_correct = _normalise_answer(answer) == _normalise_answer(question.correct_answer)
                graded_count += 1
                if is_correct:
                    score += 1

            results.append({
                'question': question,
                'answer': answer,
                'is_correct': is_correct,
            })

    return render(
        request,
        'practice/by_topic.html',
        {
            'topic': topic,
            'subject': topic.subject,
            'questions': questions,
            'submitted': submitted,
            'results': results,
            'score': score,
            'graded_count': graded_count,
        },
    )


def practice_list(request):
    query = request.GET.get('q', '').strip()[:100]
    subject_id = request.GET.get('subject', '').strip()
    topic_id = request.GET.get('topic', '').strip()

    questions = (
        PracticeQuestion.objects.filter(status=PracticeQuestion.Status.PUBLISHED)
        .select_related('topic', 'topic__subject')
        .order_by(
            'topic__subject__title',
            'topic__order',
            'topic__title',
            'id',
        )
    )

    if query:
        questions = questions.filter(
            Q(question__icontains=query)
            | Q(topic__title__icontains=query)
            | Q(topic__subject__title__icontains=query)
        )

    if subject_id.isdigit():
        questions = questions.filter(topic__subject_id=int(subject_id))

    if topic_id.isdigit():
        questions = questions.filter(topic_id=int(topic_id))

    from apps.subjects.models import Subject

    subjects = Subject.objects.filter(
        status=Subject.Status.PUBLISHED
    ).order_by('order', 'title')

    topics = Topic.objects.filter(
        status=Topic.Status.PUBLISHED
    ).select_related('subject').order_by(
        'subject__order',
        'subject__title',
        'order',
        'title',
    )

    return render(
        request,
        'practice/list.html',
        {
            'questions': questions[:100],
            'subjects': subjects,
            'topics': topics,
            'query': query,
            'selected_subject_id': subject_id if subject_id.isdigit() else '',
            'selected_topic_id': topic_id if topic_id.isdigit() else '',
        },
    )
