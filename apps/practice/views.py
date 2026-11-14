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
        subject__status=Topic.Status.PUBLISHED,
    )

    questions = list(
        topic.questions.filter(
            status=PracticeQuestion.Status.PUBLISHED
        ).order_by('id')
    )

    if not questions:
        return render(
            request,
            'practice/by_topic.html',
            {
                'topic': topic,
                'subject': topic.subject,
                'questions': [],
                'submitted': False,
                'finished': False,
                'results': [],
                'score': 0,
                'graded_count': 0,
            },
        )

    session_key = f'practice_topic_{topic.id}'
    question_map = {question.id: question for question in questions}
    practice_session = request.session.get(session_key)

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

    selected_questions = [
        question_map[question_id]
        for question_id in practice_session.get('question_ids', [])
        if question_id in question_map
    ]

    if not selected_questions:
        request.session.pop(session_key, None)
        return render(
            request,
            'practice/by_topic.html',
            {
                'topic': topic,
                'subject': topic.subject,
                'questions': [],
                'submitted': False,
                'finished': False,
                'results': [],
                'score': 0,
                'graded_count': 0,
            },
        )

    current_index = practice_session.get('current_index', 0)
    current_index = max(0, min(current_index, len(selected_questions) - 1))
    current_question = selected_questions[current_index]
    question_key = str(current_question.id)

    submitted = bool(practice_session.get('checked', {}).get(question_key, False))
    current_answer = practice_session.get('answers', {}).get(question_key, '')
    is_correct = None
    answer_error = ''

    if submitted and current_question.type in (
        PracticeQuestion.QType.MCQ,
        PracticeQuestion.QType.SHORT,
    ):
        is_correct = (
            _normalise_answer(current_answer)
            == _normalise_answer(current_question.correct_answer)
        )

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()

        if action == 'check' and not submitted:
            answer = request.POST.get(f'question_{current_question.id}', '').strip()
            current_answer = answer

            if current_question.type == PracticeQuestion.QType.MCQ:
                valid_options = {
                    str(option).strip()
                    for option in (current_question.options or [])
                }
                valid_answer = answer in valid_options
                if not valid_answer:
                    answer_error = 'Please select one of the available options.'
            elif not answer:
                valid_answer = False
                answer_error = 'Please enter your answer before checking it.'
            else:
                valid_answer = True

            if valid_answer:
                practice_session.setdefault('answers', {})[question_key] = answer
                practice_session.setdefault('checked', {})[question_key] = True
                submitted = True

                if current_question.type in (
                    PracticeQuestion.QType.MCQ,
                    PracticeQuestion.QType.SHORT,
                ):
                    is_correct = (
                        _normalise_answer(answer)
                        == _normalise_answer(current_question.correct_answer)
                    )
                    if is_correct:
                        practice_session['score'] = (
                            practice_session.get('score', 0) + 1
                        )

                request.session[session_key] = practice_session
                request.session.modified = True

        elif action == 'next':
            if submitted and current_index < len(selected_questions) - 1:
                practice_session['current_index'] = current_index + 1
                request.session[session_key] = practice_session
                request.session.modified = True
                current_index += 1
                current_question = selected_questions[current_index]
                question_key = str(current_question.id)
                current_answer = practice_session.get('answers', {}).get(
                    question_key, ''
                )
                submitted = bool(
                    practice_session.get('checked', {}).get(question_key, False)
                )
                is_correct = None
                if submitted and current_question.type in (
                    PracticeQuestion.QType.MCQ,
                    PracticeQuestion.QType.SHORT,
                ):
                    is_correct = (
                        _normalise_answer(current_answer)
                        == _normalise_answer(current_question.correct_answer)
                    )

        elif action == 'finish':
            all_questions_checked = all(
                practice_session.get('checked', {}).get(str(question.id), False)
                for question in selected_questions
            )
            is_last_question = current_index == len(selected_questions) - 1

            if submitted and is_last_question and all_questions_checked:
                score = practice_session.get('score', 0)
                graded_count = sum(
                    question.type in (
                        PracticeQuestion.QType.MCQ,
                        PracticeQuestion.QType.SHORT,
                    )
                    for question in selected_questions
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
    checked = bool(
        practice_session.get('checked', {}).get(str(current_question.id), False)
    )
    graded_count = sum(
        question.type in (
            PracticeQuestion.QType.MCQ,
            PracticeQuestion.QType.SHORT,
        )
        for question in selected_questions
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
            'submitted': checked,
            'finished': False,
            'current_answer': current_answer,
            'is_correct': is_correct,
            'checked': checked,
            'answer_error': answer_error,
            'score': practice_session.get('score', 0),
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
        'subject__title',
        'subject__order',
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
