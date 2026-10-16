from django.urls import path

from .views import FooterSettingsView


urlpatterns = [
    path("footer/", FooterSettingsView.as_view(), name="site-footer"),
]
