from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.learning.models import LearningResource
from apps.opportunities.models import Opportunity
from apps.practice.models import PracticeQuestion
from apps.subjects.models import Subject, Topic


class GlobalSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(
            title='Information Technology',
            slug='information-technology',
            description='University technology studies.',
            discipline='Computing',
            status=Subject.Status.PUBLISHED,
        )
        cls.topic = Topic.objects.create(
            subject=cls.subject,
            title='Introduction to Networking',
            slug='introduction-to-networking',
            summary='Learn how computer networks communicate.',
            status=Topic.Status.PUBLISHED,
        )
        cls.resource = LearningResource.objects.create(
            topic=cls.topic,
            title='Understanding Network Routing',
            slug='understanding-network-routing',
            summary='A guide to moving data between networks.',
            key_concepts='packet switching, routing, network paths',
            content='<p>Learning material about routing.</p>',
            status=LearningResource.Status.PUBLISHED,
        )
        cls.live_opportunity = Opportunity.objects.create(
            title='Technology Scholarship',
            slug='technology-scholarship',
            description='Financial support for technology students.',
            category=Opportunity.Category.SCHOLARSHIP,
            eligibility='University students studying computing.',
            deadline=timezone.now() + timedelta(days=30),
            location='Kampala',
            status=Opportunity.Status.ACTIVE,
        )
        cls.expired_opportunity = Opportunity.objects.create(
            title='Old Technology Scholarship',
            slug='old-technology-scholarship',
            description='This opportunity is no longer available.',
            category=Opportunity.Category.SCHOLARSHIP,
            deadline=timezone.now() - timedelta(days=1),
            status=Opportunity.Status.EXPIRED,
        )

    def test_search_finds_material_by_key_concept(self):
        response = self.client.get('/search/?q=packet')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.resource, response.context['results']['resources'])
        self.assertContains(response, self.resource.title)

    def test_search_finds_topics_and_materials_by_subject_name(self):
        response = self.client.get('/search/?q=Information%20Technology')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.topic, response.context['results']['topics'])
        self.assertIn(self.resource, response.context['results']['resources'])

    def test_search_shows_current_opportunities_only(self):
        response = self.client.get('/search/?q=Technology')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.live_opportunity, response.context['results']['opportunities'])
        self.assertNotIn(self.expired_opportunity, response.context['results']['opportunities'])

    def test_no_results_provides_direct_navigation_links(self):
        response = self.client.get('/search/?q=no-matching-result')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['has_results'])
        self.assertContains(response, 'No matches')
        self.assertContains(response, 'href="/subjects/"')
        self.assertContains(response, 'href="/learn/"')
        self.assertContains(response, 'href="/practice/"')

    def test_search_page_without_query_shows_starting_points(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Start with what you need')
        self.assertContains(response, 'href="/opportunities/"')
        self.assertContains(response, 'href="/news/"')

def test_search_matches_lesson_body_and_multiple_terms(self):
        resource = LearningResource.objects.create(
            topic=self.topic,
            title='Accessible Markup',
            slug='accessible-markup',
            summary='A guide to semantic elements.',
            objectives='Use semantic HTML in a document',
            key_concepts='HTML, semantics, accessibility',
            content='<p>Semantic elements give structure and meaning to a web page.</p>',
            status=LearningResource.Status.PUBLISHED,
        )

        response = self.client.get('/search/?q=semantic%20elements')
        self.assertEqual(response.status_code, 200)
        self.assertIn(resource, response.context['results']['resources'])

    def test_title_matches_are_ranked_ahead_of_body_only_matches(self):
        title_match = LearningResource.objects.create(
            topic=self.topic,
            title='Network Routing Basics',
            slug='network-routing-basics',
            summary='Learn the foundations.',
            content='<p>Moving information across networks.</p>',
            status=LearningResource.Status.PUBLISHED,
        )
        body_match = LearningResource.objects.create(
            topic=self.topic,
            title='Moving Data',
            slug='moving-data',
            summary='An overview.',
            content='<p>Network routing makes this possible.</p>',
            status=LearningResource.Status.PUBLISHED,
        )

        response = self.client.get('/search/?q=Network%20Routing')
        results = response.context['results']['resources']
        self.assertLess(results.index(title_match), results.index(body_match))

    def test_no_results_offer_real_published_learning_recommendations(self):
        resource = LearningResource.objects.create(
            topic=self.topic,
            title='Recommended Networking Introduction',
            slug='recommended-networking-introduction',
            summary='Start learning the basics.',
            content='<p>An introduction.</p>',
            status=LearningResource.Status.PUBLISHED,
            is_featured=True,
        )

        response = self.client.get('/search/?q=no-result-will-match')
        self.assertEqual(response.status_code, 200)
        self.assertIn(resource, response.context['recommended_resources'])
        self.assertContains(response, resource.title)

    def test_search_includes_practice_questions_without_exposing_answers(self):
        question = PracticeQuestion.objects.create(
            topic=self.topic,
            type=PracticeQuestion.QType.MCQ,
            question='Which device forwards network packets?',
            options=['Router', 'Keyboard', 'Monitor'],
            correct_answer='Router',
            explanation='Routers forward packets between networks.',
            status=PracticeQuestion.Status.PUBLISHED,
        )

        response = self.client.get('/search/?q=forwards%20network')
        self.assertEqual(response.status_code, 200)
        self.assertIn(question, response.context['results']['practice'])
        self.assertContains(response, question.question)
        self.assertNotContains(response, question.explanation)
