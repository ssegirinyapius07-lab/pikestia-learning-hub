from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Opportunity


class PublicOpportunityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.verified = Opportunity.objects.create(
            title='Verified Student Scholarship',
            slug='verified-student-scholarship',
            description='A current scholarship listing.',
            category=Opportunity.Category.SCHOLARSHIP,
            status=Opportunity.Status.ACTIVE,
            is_verified=True,
            deadline=timezone.now() + timedelta(days=14),
        )
        cls.unverified = Opportunity.objects.create(
            title='Unverified Student Internship',
            slug='unverified-student-internship',
            description='This listing has not been checked.',
            category=Opportunity.Category.INTERNSHIP,
            status=Opportunity.Status.ACTIVE,
            is_verified=False,
        )
        cls.expired = Opportunity.objects.create(
            title='Expired Verified Workshop',
            slug='expired-verified-workshop',
            description='The deadline has passed.',
            category=Opportunity.Category.WORKSHOP,
            status=Opportunity.Status.ACTIVE,
            is_verified=True,
            deadline=timezone.now() - timedelta(days=1),
        )

    def test_public_list_shows_only_verified_current_opportunities(self):
        response = self.client.get('/opportunities/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.verified.title)
        self.assertNotContains(response, self.unverified.title)
        self.assertNotContains(response, self.expired.title)

    def test_unverified_opportunity_detail_is_not_public(self):
        response = self.client.get(f'/opportunities/{self.unverified.slug}/')
        self.assertEqual(response.status_code, 404)

    def test_verified_opportunity_detail_is_public(self):
        response = self.client.get(f'/opportunities/{self.verified.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Verified')

    def test_new_opportunities_start_as_drafts(self):
        opportunity = Opportunity.objects.create(
            title='New Draft Opportunity',
            slug='new-draft-opportunity',
            description='This should not be public yet.',
            category=Opportunity.Category.TRAINING,
        )
        self.assertEqual(opportunity.status, Opportunity.Status.DRAFT)
        self.assertIsNone(opportunity.published_at)
