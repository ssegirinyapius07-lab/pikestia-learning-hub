from datetime import timedelta

from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.utils import timezone

from apps.accounts.models import User
from apps.learning.models import LearningResource
from apps.news.models import NewsArticle
from apps.practice.models import PracticeQuestion
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
            is_verified=True,
        )
        cls.expired_opportunity = Opportunity.objects.create(
            title='Old Technology Scholarship',
            slug='old-technology-scholarship',
            description='This opportunity is no longer available.',
            category=Opportunity.Category.SCHOLARSHIP,
            deadline=timezone.now() - timedelta(days=1),
            status=Opportunity.Status.EXPIRED,
            is_verified=True,
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

    def test_search_hides_active_but_unverified_opportunities(self):
        unverified = Opportunity.objects.create(
            title='Unverified Technology Internship',
            slug='unverified-technology-internship',
            description='This listing has not been checked.',
            category=Opportunity.Category.INTERNSHIP,
            status=Opportunity.Status.ACTIVE,
            is_verified=False,
        )
        response = self.client.get('/search/?q=Unverified')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(unverified, response.context['results']['opportunities'])

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



class AdminRolePermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_user(
            email='admin@example.org',
            password='Strong-admin-password-123',
            role=User.Role.ADMIN,
        )
        cls.publisher = User.objects.create_user(
            email='publisher@example.org',
            password='Strong-publisher-password-123',
            role=User.Role.PUBLISHER,
        )
        cls.other_publisher = User.objects.create_user(
            email='other-publisher@example.org',
            password='Strong-other-password-123',
            role=User.Role.PUBLISHER,
        )
        cls.student = User.objects.create_user(
            email='student@example.org',
            password='Strong-student-password-123',
            role=User.Role.USER,
        )
        cls.subject = Subject.objects.create(
            title='Permission Test Computing',
            slug='permission-test-computing',
            discipline='Computing',
            status=Subject.Status.PUBLISHED,
        )
        cls.topic = Topic.objects.create(
            subject=cls.subject,
            title='Permission Test Topic',
            slug='permission-test-topic',
            status=Topic.Status.PUBLISHED,
        )
        cls.owned_resource = LearningResource.objects.create(
            topic=cls.topic,
            title='Publisher A Resource',
            slug='publisher-a-resource',
            content='<p>Owned resource.</p>',
            created_by=cls.publisher,
            status=LearningResource.Status.REVIEW,
        )
        cls.other_resource = LearningResource.objects.create(
            topic=cls.topic,
            title='Publisher B Resource',
            slug='publisher-b-resource',
            content='<p>Other resource.</p>',
            created_by=cls.other_publisher,
            status=LearningResource.Status.REVIEW,
        )
        cls.owned_article = NewsArticle.objects.create(
            title='Publisher A Article',
            slug='publisher-a-article',
            body_raw='<p>Owned article.</p>',
            author=cls.publisher,
            status=NewsArticle.Status.REVIEW,
        )
        cls.other_article = NewsArticle.objects.create(
            title='Publisher B Article',
            slug='publisher-b-article',
            body_raw='<p>Other article.</p>',
            author=cls.other_publisher,
            status=NewsArticle.Status.REVIEW,
        )

    def request_for(self, user):
        request = RequestFactory().get('/admin/')
        request.user = user
        return request

    def test_normal_user_is_not_staff_and_cannot_open_admin(self):
        self.assertFalse(self.student.is_staff)
        self.client.force_login(self.student)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_publisher_can_see_only_learning_and_news_admin_modules(self):
        request = self.request_for(self.publisher)
        resource_admin = admin.site._registry[LearningResource]
        news_admin = admin.site._registry[NewsArticle]
        subject_admin = admin.site._registry[Subject]
        practice_admin = admin.site._registry[PracticeQuestion]
        opportunity_admin = admin.site._registry[Opportunity]
        user_admin = admin.site._registry[User]

        self.assertTrue(resource_admin.has_module_permission(request))
        self.assertTrue(news_admin.has_module_permission(request))
        self.assertFalse(subject_admin.has_module_permission(request))
        self.assertFalse(practice_admin.has_module_permission(request))
        self.assertFalse(opportunity_admin.has_module_permission(request))
        self.assertFalse(user_admin.has_module_permission(request))

    def test_publisher_queryset_contains_only_owned_content(self):
        request = self.request_for(self.publisher)
        resource_admin = admin.site._registry[LearningResource]
        news_admin = admin.site._registry[NewsArticle]

        self.assertEqual(
            list(resource_admin.get_queryset(request)),
            [self.owned_resource],
        )
        self.assertEqual(
            list(news_admin.get_queryset(request)),
            [self.owned_article],
        )

    def test_publisher_cannot_change_or_delete_another_publishers_content(self):
        request = self.request_for(self.publisher)
        resource_admin = admin.site._registry[LearningResource]
        news_admin = admin.site._registry[NewsArticle]

        self.assertTrue(resource_admin.has_change_permission(request, self.owned_resource))
        self.assertFalse(resource_admin.has_change_permission(request, self.other_resource))
        self.assertFalse(resource_admin.has_delete_permission(request, self.owned_resource))

        self.assertTrue(news_admin.has_change_permission(request, self.owned_article))
        self.assertFalse(news_admin.has_change_permission(request, self.other_article))
        self.assertFalse(news_admin.has_delete_permission(request, self.owned_article))

    def test_publisher_submissions_are_owned_and_sent_to_review(self):
        request = self.request_for(self.publisher)
        resource_admin = admin.site._registry[LearningResource]
        news_admin = admin.site._registry[NewsArticle]

        resource = LearningResource(
            topic=self.topic,
            title='New Publisher Resource',
            slug='new-publisher-resource',
            content_raw='<p>New content.</p>',
            status=LearningResource.Status.PUBLISHED,
        )
        resource_admin.save_model(request, resource, form=None, change=False)
        resource.refresh_from_db()
        self.assertEqual(resource.created_by, self.publisher)
        self.assertEqual(resource.status, LearningResource.Status.REVIEW)

        article = NewsArticle(
            title='New Publisher Article',
            slug='new-publisher-article',
            body_raw='<p>New article.</p>',
            status=NewsArticle.Status.PUBLISHED,
            featured=True,
        )
        news_admin.save_model(request, article, form=None, change=False)
        article.refresh_from_db()
        self.assertEqual(article.author, self.publisher)
        self.assertEqual(article.status, NewsArticle.Status.REVIEW)
        self.assertFalse(article.featured)
        self.assertIsNone(article.published_at)

    def test_administrator_retains_full_admin_permissions(self):
        request = self.request_for(self.admin_user)
        for model in (
            LearningResource,
            NewsArticle,
            Subject,
            PracticeQuestion,
            Opportunity,
            User,
        ):
            model_admin = admin.site._registry[model]
            self.assertTrue(model_admin.has_module_permission(request))
            self.assertTrue(model_admin.has_add_permission(request))


    def test_publisher_can_select_only_published_topics(self):
        unpublished_topic = Topic.objects.create(
            subject=self.subject,
            title='Unpublished Topic',
            slug='unpublished-topic-for-publisher',
            status=Topic.Status.DRAFT,
        )
        request = self.request_for(self.publisher)
        resource_admin = admin.site._registry[LearningResource]
        topic_field = resource_admin.formfield_for_foreignkey(
            LearningResource._meta.get_field('topic'),
            request,
        )
        self.assertIn(self.topic, topic_field.queryset)
        self.assertNotIn(unpublished_topic, topic_field.queryset)
