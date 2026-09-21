from django.test import TestCase

from apps.subjects.models import Subject, Topic

from .models import LearningResource


class LearningResourceListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.it = Subject.objects.create(
            title='Information Technology',
            slug='information-technology',
            description='Technology studies.',
            discipline='Information Technology',
            status=Subject.Status.PUBLISHED,
        )
        cls.business = Subject.objects.create(
            title='Business Administration',
            slug='business-administration',
            description='Business studies.',
            discipline='Business',
            status=Subject.Status.PUBLISHED,
        )
        cls.programming = Topic.objects.create(
            subject=cls.it,
            title='Programming Fundamentals',
            slug='programming-fundamentals',
            summary='Programming basics.',
            status=Topic.Status.PUBLISHED,
        )
        cls.databases = Topic.objects.create(
            subject=cls.it,
            title='Database Systems',
            slug='database-systems',
            summary='Database concepts.',
            status=Topic.Status.PUBLISHED,
        )
        cls.accounting = Topic.objects.create(
            subject=cls.business,
            title='Financial Accounting',
            slug='financial-accounting',
            summary='Accounting basics.',
            status=Topic.Status.PUBLISHED,
        )

        for number in range(20):
            LearningResource.objects.create(
                topic=cls.programming if number < 10 else cls.databases,
                title=f'Programming Material {number + 1}',
                slug=f'material-{number + 1}',
                summary='Python and programming concepts.' if number == 0 else 'University study material.',
                content='<p>Safe learning content.</p>',
                key_concepts='python, programming' if number == 0 else '',
                status=LearningResource.Status.PUBLISHED,
                order=number,
            )

        LearningResource.objects.create(
            topic=cls.accounting,
            title='Accounting Draft',
            slug='accounting-draft',
            summary='Not publicly visible.',
            content='<p>Draft content.</p>',
            status=LearningResource.Status.DRAFT,
        )

    def test_library_is_paginated(self):
        response = self.client.get('/learn/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 20)
        self.assertEqual(len(response.context['resources']), 18)
        self.assertContains(response, 'Learning Materials')

    def test_search_matches_resource_metadata(self):
        response = self.client.get('/learn/?q=python')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
        self.assertContains(response, 'Programming Material 1')

    def test_subject_filter_limits_results(self):
        response = self.client.get(f'/learn/?subject={self.business.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 0)

    def test_topic_filter_limits_results(self):
        response = self.client.get(f'/learn/?topic={self.programming.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 10)

    def test_unpublished_materials_are_hidden(self):
        response = self.client.get('/learn/?q=not%20publicly%20visible')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 0)
