"""Mail-only anonymous appeals. Do not persist or log request payloads."""
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.crypto import salted_hmac
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class AnonymousMessageSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField(max_length=5000)
    name = serializers.CharField(max_length=120, required=False, allow_blank=True, default='')
    email = serializers.EmailField(max_length=254, required=False, allow_blank=True, default='')
    website = serializers.CharField(max_length=200, required=False, allow_blank=True, default='')

    def validate_subject(self, value):
        if '\r' in value or '\n' in value:
            raise serializers.ValidationError('Invalid subject.')
        return value


class AppealThrottle(AnonRateThrottle):
    scope = 'anonymous_message'

    def get_cache_key(self, request, view):
        ident = salted_hmac("anonymous-appeal", self.get_ident(request)).hexdigest()
        return self.cache_format % {"scope": self.scope, "ident": ident}

    def get_rate(self):
        return settings.ANONYMOUS_MESSAGE_RATE


class AnonymousMessageView(APIView):
    serializer_class = AnonymousMessageSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [AppealThrottle]

    def post(self, request):
        serializer = AnonymousMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if data['website']:
            return Response({'detail': 'Message accepted.'})
        recipient = settings.ANONYMOUS_MESSAGE_RECIPIENT
        if not recipient:
            logger.error('anonymous_message_unconfigured')
            return Response({'detail': 'Delivery unavailable.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        # Contact data stays in the mail body and Reply-To, never in the service sender.
        body = '\n'.join([
            f'Date: {timezone.now().isoformat()}',
            f'Subject: {data["subject"]}',
            f'Name: {data["name"] or "—"}',
            f'Contact email: {data["email"] or "—"}',
            '', data['message'],
        ])
        try:
            delivered = EmailMessage(
                subject=f'[University appeal] {data["subject"]}', body=body,
                from_email=settings.DEFAULT_FROM_EMAIL, to=[recipient],
                reply_to=[data['email']] if data['email'] else [],
            ).send(fail_silently=False)
            if delivered != 1:
                raise RuntimeError('No message accepted by provider')
        except Exception:
            # SMTP exception text can contain addresses or content. Log only a fixed event.
            logger.error('anonymous_message_delivery_failed')
            return Response({'detail': 'Delivery failed. Please retry.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        logger.info('anonymous_message_delivered')
        return Response({'detail': 'Message sent.'})
