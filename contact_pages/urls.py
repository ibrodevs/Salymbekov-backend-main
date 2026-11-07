from django.urls import path

from .anonymous import AnonymousMessageView
from .views import FooterSettingsView


urlpatterns = [
    path("anonymous-message/", AnonymousMessageView.as_view(), name="anonymous-message"),
    path("footer/", FooterSettingsView.as_view(), name="site-footer"),
]
