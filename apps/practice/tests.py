from django.test import TestCase

from apps.subjects.models import Subject, Topic

from .models import PracticeQuestion


class PracticeTopicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(
            title='Information Technology',
            slug='information-technology',
            discipline='Information Technology',
            status=Subject.Status.PUBLISHED,
        )
        cls.topic = Topic.objects.create(
            subject=cls.subject,
            title='Programming Fundamentals',
            slug='programming-fundamentals',
            status=Topic.Status.PUBLISHED,
        )
        cls.question = PracticeQuestion.objects.create(
            topic=cls.topic,
            type=PracticeQuestion.QType.MCQ,
            question='Which language is used in this example?',
            options=['Python', 'HTML', 'SQL'],
            correct_answer='Python',
            explanation='Python is the correct answer.',
            status=PracticeQuestion.Status.PUBLISHED,
        )

    def practice_url(self):
        return '/practice/information-technology/programming-fundamentals/'

    def test_practice_page_does_not_expose_answer_before_submission(self):
        response = self.client.get(self.practice_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.question)
        self.assertNotContains(response, 'Python is the correct answer.')
        self.assertNotContains(response, 'Model answer:')

    def test_correct_answer_is_graded_server_side(self):
        response = self.client.post(
            self.practice_url(),
            {
                'action': 'check',
                f'question_{self.question.id}': 'Python',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 1)
        self.assertEqual(response.context['graded_count'], 1)
        self.assertTrue(response.context['checked'])
        self.assertContains(response, 'Correct')
        self.assertContains(response, 'Python is the correct answer.')

    def test_incorrect_answer_is_graded_server_side(self):
        response = self.client.post(
            self.practice_url(),
            {
                'action': 'check',
                f'question_{self.question.id}': 'HTML',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 0)
        self.assertEqual(response.context['graded_count'], 1)
        self.assertTrue(response.context['checked'])
        self.assertContains(response, 'Review this answer')
        self.assertContains(response, 'Python is the correct answer.')

    def test_answer_is_not_graded_when_action_is_missing(self):
        response = self.client.post(
            self.practice_url(),
            {f'question_{self.question.id}': 'Python'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 0)
        self.assertFalse(response.context['checked'])
        self.assertNotContains(response, 'Python is the correct answer.')

    def test_invalid_multiple_choice_option_is_rejected(self):
        response = self.client.post(
            self.practice_url(),
            {
                'action': 'check',
                f'question_{self.question.id}': 'JavaScript',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['checked'])
        self.assertEqual(response.context['score'], 0)
        self.assertContains(response, 'Please select one of the available options.')

    def test_already_checked_answer_cannot_be_changed_or_graded_twice(self):
        self.client.post(
            self.practice_url(),
            {
                'action': 'check',
                f'question_{self.question.id}': 'Python',
            },
        )
        response = self.client.post(
            self.practice_url(),
            {
                'action': 'check',
                f'question_{self.question.id}': 'HTML',
            },
        )
        self.assertEqual(response.context['score'], 1)
        self.assertEqual(response.context['current_answer'], 'Python')
        self.assertTrue(response.context['is_correct'])

    def test_learner_cannot_skip_an_unchecked_question(self):
        second_question = PracticeQuestion.objects.create(
            topic=self.topic,
            type=PracticeQuestion.QType.MCQ,
            question='What does SQL primarily manage?',
            options=['Databases', 'Images', 'Sound'],
            correct_answer='Databases',
            status=PracticeQuestion.Status.PUBLISHED,
        )
        response = self.client.post(
            self.practice_url(),
            {'action': 'next'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_question'].id, self.question.id)
        self.assertEqual(response.context['total_questions'], 2)
        self.assertNotEqual(response.context['current_question'].id, second_question.id)

    def test_learner_cannot_finish_before_completing_the_questions(self):
        response = self.client.post(
            self.practice_url(),
            {'action': 'finish'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['finished'])
        self.assertEqual(response.context['current_question'].id, self.question.id)

    def test_exercise_can_be_checked_without_inflating_automatic_score(self):
        exercise_topic = Topic.objects.create(
            subject=self.subject,
            title='Written Exercises',
            slug='written-exercises',
            status=Topic.Status.PUBLISHED,
        )
        exercise = PracticeQuestion.objects.create(
            topic=exercise_topic,
            type=PracticeQuestion.QType.EXERCISE,
            question='Explain why database backups are important.',
            explanation='Backups support recovery after data loss.',
            status=PracticeQuestion.Status.PUBLISHED,
        )
        url = '/practice/information-technology/written-exercises/'
        response = self.client.post(
            url,
            {
                'action': 'check',
                f'question_{exercise.id}': 'They help recover lost data.',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['checked'])
        self.assertIsNone(response.context['is_correct'])
        self.assertEqual(response.context['score'], 0)
        self.assertEqual(response.context['graded_count'], 0)
        self.assertContains(response, 'Compare with the model answer')

    def test_single_question_attempt_can_finish_after_checking(self):
        self.client.post(
            self.practice_url(),
            {
                'action': 'check',
                f'question_{self.question.id}': 'Python',
            },
        )
        response = self.client.post(self.practice_url(), {'action': 'finish'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['finished'])
        self.assertEqual(response.context['score'], 1)
        self.assertEqual(response.context['graded_count'], 1)
