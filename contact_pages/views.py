from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView

from .models import FooterSettings
from .serializers import FooterSettingsSerializer


class FooterSettingsView(RetrieveAPIView):
    serializer_class = FooterSettingsSerializer

    def get_object(self):
        return get_object_or_404(FooterSettings, is_active=True, key="main")
