from types import SimpleNamespace

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core import mail
from django.test import RequestFactory, TestCase, override_settings

from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import AuditLog
from .views import _logout_other_sessions


User = get_user_model()


class AuthenticationConfigurationTests(TestCase):
    def test_google_account_selection_is_enabled(self):
        google = settings.SOCIALACCOUNT_PROVIDERS['google']
        self.assertEqual(google['AUTH_PARAMS'].get('prompt'), 'select_account')

    def test_google_identity_is_trusted_for_verified_email_authentication(self):
        google = settings.SOCIALACCOUNT_PROVIDERS['google']
        self.assertTrue(settings.SOCIALACCOUNT_EMAIL_AUTHENTICATION)
        self.assertTrue(settings.SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT)
        self.assertTrue(google.get('EMAIL_AUTHENTICATION'))
        self.assertTrue(google.get('VERIFIED_EMAIL'))

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_email_signup_requires_verification_and_sends_email(self):
        response = self.client.post(
            '/accounts/signup/',
            {
                'email': 'newstudent@example.org',
                'full_name': 'New Student',
                'password1': 'A-strong-test-password-123',
                'password2': 'A-strong-test-password-123',
            },
        )

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='newstudent@example.org')
        email_address = EmailAddress.objects.get(user=user, email=user.email)

        self.assertFalse(email_address.verified)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Pikestia Learning Hub', mail.outbox[0].subject)

    def test_social_adapter_maps_google_name(self):
        adapter = DefaultSocialAccountAdapter()
        data = {
            'email': 'googleuser@example.org',
            'name': 'Google User',
        }

        request = RequestFactory().get('/accounts/login/')

        user = adapter.populate_user(
            request,
            SimpleNamespace(
                user=User(email='googleuser@example.org'),
                account=SimpleNamespace(extra_data=data),
            ),
            data,
        )

        self.assertEqual(user.full_name, 'Google User')


class SecurityBehaviorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='student@example.org',
            password='Initial-password-123',
            full_name='Test Student',
        )

    def test_password_change_revokes_other_sessions(self):
        device_a = self.client_class()
        device_b = self.client_class()

        self.assertTrue(device_a.login(email=self.user.email, password='Initial-password-123'))
        self.assertTrue(device_b.login(email=self.user.email, password='Initial-password-123'))

        other_session_key = device_b.session.session_key
        self.assertTrue(
            Session.objects.filter(
                session_key=other_session_key,
                expire_date__gt=timezone.now(),
            ).exists()
        )

        response = device_a.post(
            '/accounts/settings/password/',
            {
                'old_password': 'Initial-password-123',
                'new_password1': 'New-password-456',
                'new_password2': 'New-password-456',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(device_a.session.get('_auth_user_id'))
        self.assertFalse(
            Session.objects.filter(session_key=other_session_key).exists()
        )
        self.assertEqual(
            AuditLog.objects.filter(
                user=self.user,
                action='password_change',
            ).count(),
            1,
        )

        device_b_response = device_b.get('/accounts/profile/')
        self.assertEqual(device_b_response.status_code, 302)
        self.assertIn('/accounts/login/', device_b_response.url)

    def test_theme_stays_with_user_and_survives_logout(self):
        self.user.display_mode = User.DisplayMode.DARK
        self.user.save(update_fields=['display_mode'])

        self.assertTrue(
            self.client.login(
                email=self.user.email,
                password='Initial-password-123',
            )
        )

        authenticated_response = self.client.get('/')
        self.assertEqual(authenticated_response.context['display_mode'], 'dark')
        self.assertEqual(
            authenticated_response.cookies['display_mode'].value,
            'dark',
        )

        logout_response = self.client.post('/accounts/logout/')
        self.assertEqual(logout_response.status_code, 302)

        anonymous_response = self.client.get('/')
        self.assertEqual(anonymous_response.context['display_mode'], 'dark')
        self.assertEqual(
            anonymous_response.cookies['display_mode'].value,
            'dark',
        )

    def test_one_click_account_logout(self):
        self.assertTrue(
            self.client.login(
                email=self.user.email,
                password='Initial-password-123',
            )
        )

        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

        protected = self.client.get('/accounts/profile/')
        self.assertEqual(protected.status_code, 302)
        self.assertIn('/accounts/login/', protected.url)

    def test_password_change_keeps_current_device_signed_in(self):
        self.assertTrue(
            self.client.login(
                email=self.user.email,
                password='Initial-password-123',
            )
        )

        response = self.client.post(
            '/accounts/settings/password/',
            {
                'old_password': 'Initial-password-123',
                'new_password1': 'New-password-456',
                'new_password2': 'New-password-456',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(self.client.session.get('_auth_user_id'))

        protected = self.client.get('/accounts/profile/')
        self.assertEqual(protected.status_code, 200)
