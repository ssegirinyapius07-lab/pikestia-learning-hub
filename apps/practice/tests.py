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

    def test_practice_page_does_not_expose_answer_before_submission(self):
        response = self.client.get('/practice/information-technology/programming-fundamentals/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.question)
        self.assertNotContains(response, 'Python is the correct answer.')
        self.assertNotContains(response, '<p><strong>Model answer:</strong> Python</p>')

    def test_correct_answer_is_graded_server_side(self):
        response = self.client.post(
            '/practice/information-technology/programming-fundamentals/',
            {f'question_{self.question.id}': 'Python'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 1)
        self.assertEqual(response.context['graded_count'], 1)
        self.assertContains(response, 'Correct')
        self.assertContains(response, 'Python is the correct answer.')

    def test_incorrect_answer_is_graded_server_side(self):
        response = self.client.post(
            '/practice/information-technology/programming-fundamentals/',
            {f'question_{self.question.id}': 'HTML'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 0)
        self.assertEqual(response.context['graded_count'], 1)
        self.assertContains(response, 'Review this answer')
        self.assertContains(response, 'Python is the correct answer.')

    def test_answer_submission_without_action_is_still_checked(self):
        response = self.client.post(
            '/practice/information-technology/programming-fundamentals/',
            {f'question_{self.question.id}': 'Python'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 1)
        self.assertContains(response, 'Correct')

    def test_written_exercise_can_be_reviewed_and_finished(self):
        exercise = PracticeQuestion.objects.create(
            topic=self.topic,
            type=PracticeQuestion.QType.EXERCISE,
            question='Explain why semantic HTML matters.',
            correct_answer='Semantic HTML gives structure and meaning to page content.',
            explanation='Meaningful elements improve structure and accessibility.',
            status=PracticeQuestion.Status.PUBLISHED,
        )
        url = '/practice/information-technology/programming-fundamentals/'

        # Check the first automatically graded question, then move on.
        first = self.client.get(url)
        self.assertEqual(first.status_code, 200)
        self.client.post(
            url,
            {'action': 'check', f'question_{self.question.id}': 'Python'},
        )
        self.client.post(url, {'action': 'next'})

        response = self.client.post(
            url,
            {'action': 'check', f'question_{exercise.id}': 'It gives page sections meaning.'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['checked'])
        self.assertContains(response, 'Compare with the model answer')
        self.assertContains(response, exercise.correct_answer)
        self.assertContains(response, 'Finish practice')

