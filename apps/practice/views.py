from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.core.search import filter_by_terms, with_title_relevance
from apps.subjects.models import Subject, Topic

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
        topic.questions.filter(
            status=PracticeQuestion.Status.PUBLISHED
        ).order_by('id')
    )

    session_key = f'practice_topic_{topic.id}'

    if request.method == 'GET' and session_key not in request.session:
        question_ids = [question.id for question in questions]

        if len(question_ids) > 10:
            import random
            question_ids = random.sample(question_ids, 10)

        request.session[session_key] = {
            'question_ids': question_ids,
            'current_index': 0,
            'answers': {},
            'checked': {},
            'score': 0,
        }

    practice_session = request.session.get(session_key)

    if not questions:
        return render(
            request,
            'practice/by_topic.html',
            {
                'topic': topic,
                'subject': topic.subject,
                'questions': [],
                'submitted': False,
                'results': [],
                'score': 0,
                'graded_count': 0,
            },
        )

    if not practice_session:
        question_ids = [question.id for question in questions]

        if len(question_ids) > 10:
            import random
            question_ids = random.sample(question_ids, 10)

        practice_session = {
            'question_ids': question_ids,
            'current_index': 0,
            'answers': {},
            'checked': {},
            'score': 0,
        }

        request.session[session_key] = practice_session

    question_map = {
        question.id: question
        for question in questions
    }

    selected_questions = [
        question_map[question_id]
        for question_id in practice_session['question_ids']
        if question_id in question_map
    ]

    if not selected_questions:
        del request.session[session_key]

        return render(
            request,
            'practice/by_topic.html',
            {
                'topic': topic,
                'subject': topic.subject,
                'questions': [],
                'submitted': False,
                'results': [],
                'score': 0,
                'graded_count': 0,
            },
        )

    current_index = practice_session.get('current_index', 0)

    if current_index >= len(selected_questions):
        current_index = len(selected_questions) - 1
        practice_session['current_index'] = current_index

    current_question = selected_questions[current_index]

    submitted = False
    is_correct = None
    current_answer = practice_session['answers'].get(
        str(current_question.id),
        '',
    )

    action = request.POST.get('action', '').strip()

    if request.method == 'POST':
        answer = request.POST.get(
            f'question_{current_question.id}',
            '',
        ).strip()

        if action == 'check':
            current_answer = answer

            practice_session['answers'][str(current_question.id)] = answer
            submitted = True

            if current_question.type in (
                PracticeQuestion.QType.MCQ,
                PracticeQuestion.QType.SHORT,
            ):
                is_correct = (
                    _normalise_answer(answer)
                    == _normalise_answer(current_question.correct_answer)
                )

                was_checked = practice_session['checked'].get(
                    str(current_question.id),
                    False,
                )

                if not was_checked:
                    practice_session['checked'][str(current_question.id)] = True

                    if is_correct:
                        practice_session['score'] += 1

            practice_session['current_index'] = current_index
            request.session[session_key] = practice_session
            request.session.modified = True

        elif action == 'next':
            practice_session['current_index'] = min(
                current_index + 1,
                len(selected_questions) - 1,
            )

            request.session[session_key] = practice_session
            request.session.modified = True

            current_index = practice_session['current_index']
            current_question = selected_questions[current_index]
            current_answer = practice_session['answers'].get(
                str(current_question.id),
                '',
            )

            submitted = False
            is_correct = None

        elif action == 'finish':
            score = practice_session.get('score', 0)
            graded_count = sum(
                1
                for question in selected_questions
                if question.type in (
                    PracticeQuestion.QType.MCQ,
                    PracticeQuestion.QType.SHORT,
                )
            )

            request.session.pop(session_key, None)

            return render(
                request,
                'practice/by_topic.html',
                {
                    'topic': topic,
                    'subject': topic.subject,
                    'questions': selected_questions,
                    'current_question': None,
                    'current_index': len(selected_questions),
                    'total_questions': len(selected_questions),
                    'submitted': True,
                    'finished': True,
                    'results': [],
                    'score': score,
                    'graded_count': graded_count,
                },
            )

    total_questions = len(selected_questions)

    checked = practice_session.get('checked', {}).get(
        str(current_question.id),
        False,
    )

    if checked:
        submitted = True

        if current_question.type in (
            PracticeQuestion.QType.MCQ,
            PracticeQuestion.QType.SHORT,
        ):
            is_correct = (
                _normalise_answer(current_answer)
                == _normalise_answer(current_question.correct_answer)
            )

    return render(
        request,
        'practice/by_topic.html',
        {
            'topic': topic,
            'subject': topic.subject,
            'questions': selected_questions,
            'current_question': current_question,
            'current_index': current_index,
            'total_questions': total_questions,
            'submitted': submitted,
            'finished': False,
            'current_answer': current_answer,
            'is_correct': is_correct,
            'checked': checked,
            'score': practice_session.get('score', 0),
            'graded_count': sum(
                1
                for question in selected_questions
                if question.type in (
                    PracticeQuestion.QType.MCQ,
                    PracticeQuestion.QType.SHORT,
                )
            ),
        },
    )


def practice_list(request):
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

    if selected_subject and selected_topic and selected_topic.subject_id != selected_subject.pk:
        topic_id = ''
        selected_topic = None

    questions = (
        PracticeQuestion.objects.filter(status=PracticeQuestion.Status.PUBLISHED)
        .filter(
            topic__status=Topic.Status.PUBLISHED,
            topic__subject__status=Subject.Status.PUBLISHED,
        )
        .filter(
            Q(topic__parent__isnull=True) | Q(topic__parent__status=Topic.Status.PUBLISHED)
        )
        .select_related('topic', 'topic__subject', 'topic__parent')
    )

    if query:
        questions = filter_by_terms(
            questions,
            query,
            (
                'question',
                'topic__title',
                'topic__summary',
                'topic__parent__title',
                'topic__subject__title',
                'topic__subject__discipline',
            ),
        )
        questions = with_title_relevance(questions, query, title_field='question')
        questions = questions.order_by(
            '_search_title_rank',
            'topic__subject__order',
            'topic__parent__order',
            'topic__order',
            'id',
        )
    else:
        questions = questions.order_by(
            'topic__subject__order',
            'topic__subject__title',
            'topic__parent__order',
            'topic__order',
            'id',
        )

    if subject_id:
        questions = questions.filter(topic__subject_id=int(subject_id))
    if topic_id:
        questions = questions.filter(topic_id=int(topic_id))

    topics = visible_topics.select_related('subject', 'parent').order_by(
        'subject__order',
        'subject__title',
        'parent__order',
        'parent__title',
        'order',
        'title',
    )

    paginator = Paginator(questions, 18)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    filter_params = {}
    if query:
        filter_params['q'] = query
    if subject_id:
        filter_params['subject'] = subject_id
    if topic_id:
        filter_params['topic'] = topic_id

    return render(
        request,
        'practice/list.html',
        {
            'questions': page_obj.object_list,
            'page_obj': page_obj,
            'subjects': subjects,
            'topics': topics,
            'query': query,
            'selected_subject_id': subject_id,
            'selected_topic_id': topic_id,
            'selected_subject': selected_subject,
            'selected_topic': selected_topic,
            'filter_query': urlencode(filter_params),
        },
    )
