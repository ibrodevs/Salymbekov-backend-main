from django.urls import path
from .views import PartnerListAPIView

urlpatterns = [
	path('partners/', PartnerListAPIView.as_view(), name='partners-list')
]
