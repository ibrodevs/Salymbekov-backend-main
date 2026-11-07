from unittest.mock import patch
from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
                   DEFAULT_FROM_EMAIL='service@example.org',
                   ANONYMOUS_MESSAGE_RECIPIENT='admin@example.org', ANONYMOUS_MESSAGE_RATE='5/hour')
class AnonymousMessageTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse('anonymous-message')

    def send(self, **data):
        return self.client.post(self.url, data, content_type='application/json')

    def test_no_identity_or_login_required(self):
        response = self.send(subject='Предложение', message='Текст обращения')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['admin@example.org'])
        self.assertEqual(mail.outbox[0].from_email, 'service@example.org')
        self.assertIn('Текст обращения', mail.outbox[0].body)
        self.assertIn('Date:', mail.outbox[0].body)

    def test_reply_to_does_not_replace_service_sender(self):
        self.send(subject='Reply', message='Hello', email='student@example.org')
        self.assertEqual(mail.outbox[0].reply_to, ['student@example.org'])
        self.assertEqual(mail.outbox[0].from_email, 'service@example.org')

    def test_required_fields_limits_and_header_injection(self):
        for payload in [{}, {'subject':' ', 'message':'text'}, {'subject':'x','message':' '},
                        {'subject':'x','message':'a'*5001}, {'subject':'x','message':'a','email':'bad'},
                        {'subject':'x\r\nBcc: victim@example.org','message':'a'}]:
            cache.clear()
            self.assertEqual(self.send(**payload).status_code, 400)
        self.assertFalse(getattr(mail, 'outbox', []))

    def test_rate_limit(self):
        for _ in range(5):
            self.assertEqual(self.send(subject='x', message='text').status_code, 200)
        self.assertEqual(self.send(subject='x', message='text').status_code, 429)
        self.assertEqual(len(mail.outbox), 5)

    def test_honeypot_never_sends(self):
        self.assertEqual(self.send(subject='x',message='x',website='spam').status_code, 200)
        self.assertFalse(getattr(mail, 'outbox', []))

    def test_provider_failure_is_retryable_and_not_logged_with_pii(self):
        with patch('contact_pages.anonymous.EmailMessage.send', side_effect=RuntimeError('secret message')):
            with self.assertLogs('contact_pages.anonymous', level='ERROR') as logs:
                self.assertEqual(self.send(subject='x',message='private').status_code, 503)
            self.assertNotIn('secret', '\n'.join(logs.output))
            self.assertNotIn('private', '\n'.join(logs.output))
        self.assertEqual(self.send(subject='x',message='private').status_code, 200)

    @override_settings(ANONYMOUS_MESSAGE_RECIPIENT='')
    def test_unconfigured_recipient_fails_without_accepting_mail(self):
        self.assertEqual(self.send(subject='x',message='text').status_code, 503)
