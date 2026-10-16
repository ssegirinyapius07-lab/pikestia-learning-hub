from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.learning.models import LearningResource
from apps.practice.models import PracticeQuestion
from .models import Subject, Topic


class HierarchicalSubjectCatalogueTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.it = Subject.objects.create(
            title='Information Technology',
            slug='information-technology',
            discipline='Science & Technology',
            description='Computing and digital systems.',
            status=Subject.Status.PUBLISHED,
        )
        cls.business = Subject.objects.create(
            title='Business Administration',
            slug='business-administration',
            discipline='Business',
            status=Subject.Status.PUBLISHED,
        )
        cls.web_design = Topic.objects.create(
            subject=cls.it,
            title='Web Design',
            slug='web-design',
            summary='Plan, structure and style accessible websites.',
            order=1,
            status=Topic.Status.PUBLISHED,
        )
        cls.html = Topic.objects.create(
            subject=cls.it,
            parent=cls.web_design,
            title='HTML Fundamentals',
            slug='html-fundamentals',
            summary='Use semantic HTML to structure a page.',
            learning_objectives='Describe document structure\\nUse headings and links',
            order=1,
            status=Topic.Status.PUBLISHED,
        )
        cls.resource = LearningResource.objects.create(
            topic=cls.html,
            title='Build a Semantic HTML Page',
            slug='build-a-semantic-html-page',
            summary='Learn headings, paragraphs, links and semantic page regions.',
            objectives='Explain semantic HTML\\nChoose appropriate elements',
            key_concepts='HTML, semantics, accessibility',
            content='<h2>Document structure</h2><p>Semantic elements describe the role of page content.</p>',
            order=1,
            status=LearningResource.Status.PUBLISHED,
        )
        cls.question = PracticeQuestion.objects.create(
            topic=cls.html,
            type=PracticeQuestion.QType.MCQ,
            question='Which element represents the main content of a page?',
            options=['main', 'span', 'br'],
            correct_answer='main',
            explanation='The main element identifies the primary content.',
            status=PracticeQuestion.Status.PUBLISHED,
        )

    def test_subject_page_shows_main_topics_not_subtopics(self):
        response = self.client.get('/subjects/information-technology/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Design')
        self.assertNotContains(response, 'HTML Fundamentals')

    def test_parent_topic_page_shows_its_subtopics_and_counts(self):
        response = self.client.get('/subjects/information-technology/web-design/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Topics in this section')
        self.assertContains(response, 'HTML Fundamentals')
        self.assertContains(response, '1 lesson')
        self.assertContains(response, '1 practice question')

    def test_child_topic_page_shows_parent_breadcrumb_and_learning_material(self):
        response = self.client.get('/subjects/information-technology/html-fundamentals/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Design')
        self.assertContains(response, self.resource.title)
        self.assertContains(
            response,
            '/learn/information-technology/html-fundamentals/build-a-semantic-html-page/',
        )
        self.assertContains(response, '/practice/information-technology/html-fundamentals/')

    def test_parent_and_child_must_share_the_same_subject(self):
        child = Topic(
            subject=self.business,
            parent=self.web_design,
            title='HTML for Business',
            slug='html-for-business',
        )
        with self.assertRaises(ValidationError):
            child.full_clean()

    def test_subtopic_cannot_be_parent_of_another_subtopic(self):
        child = Topic(
            subject=self.it,
            parent=self.html,
            title='HTML Forms',
            slug='html-forms',
        )
        with self.assertRaises(ValidationError):
            child.full_clean()

    def test_child_topic_is_not_public_when_parent_is_unpublished(self):
        self.web_design.status = Topic.Status.DRAFT
        self.web_design.save(update_fields=['status'])
        response = self.client.get('/subjects/information-technology/html-fundamentals/')
        self.assertEqual(response.status_code, 404)

    def test_removing_parent_preserves_child_topics_as_root_topics(self):
        child_id = self.html.pk
        parent_id = self.web_design.pk
        self.web_design.delete()

        surviving_child = Topic.objects.get(pk=child_id)
        self.assertIsNone(surviving_child.parent_id)
        self.assertEqual(surviving_child.subject_id, self.it.pk)
        self.assertTrue(LearningResource.objects.filter(topic=surviving_child).exists())
        self.assertFalse(Topic.objects.filter(pk=parent_id).exists())
