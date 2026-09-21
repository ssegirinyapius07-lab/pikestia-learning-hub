from django.test import TestCase

from apps.accounts.models import User

from .models import NewsArticle


class NewsArticleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            email='writer@example.com',
            password='StrongPassword123',
            full_name='Pikestia Writer',
        )
        cls.article = NewsArticle.objects.create(
            title='First Pikestia News Story',
            slug='first-pikestia-news-story',
            summary='A published campus story.',
            body_raw='<p>Useful article content.</p><script>alert("blocked")</script>',
            category=NewsArticle.Category.CAMPUS,
            author=cls.author,
            status=NewsArticle.Status.PUBLISHED,
            featured=True,
        )
        NewsArticle.objects.create(
            title='Draft Story',
            slug='draft-story',
            summary='Private draft.',
            body_raw='<p>Draft content.</p>',
            category=NewsArticle.Category.GENERAL,
            author=cls.author,
            status=NewsArticle.Status.DRAFT,
        )

    def test_published_article_gets_public_timestamp(self):
        self.assertIsNotNone(self.article.published_at)
        self.assertTrue(self.article.is_published)

    def test_article_body_is_sanitized(self):
        self.assertIn('Useful article content.', self.article.body)
        self.assertNotIn('<script>', self.article.body)

    def test_public_list_hides_drafts(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
        self.assertContains(response, self.article.title)
        self.assertNotContains(response, 'Draft Story')

    def test_search_finds_published_article(self):
        response = self.client.get('/news/?q=campus')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
        self.assertContains(response, self.article.title)

    def test_category_filter_works(self):
        response = self.client.get('/news/?category=campus')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)

    def test_draft_detail_is_not_public(self):
        response = self.client.get('/news/draft-story/')
        self.assertEqual(response.status_code, 404)
