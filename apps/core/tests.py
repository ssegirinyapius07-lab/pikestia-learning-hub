from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.learning.models import LearningResource
from apps.opportunities.models import Opportunity
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
