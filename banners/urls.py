from django.urls import path
from . import views

urlpatterns = [
    path("", views.BannerView.as_view(), name='banner-list')
               ]