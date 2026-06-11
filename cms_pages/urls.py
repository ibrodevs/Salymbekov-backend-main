from django.urls import path

from .views import PageByPathView, PageListView


urlpatterns = [
    path("pages/", PageListView.as_view(), name="cms-pages-list"),
    path("pages/by-path/", PageByPathView.as_view(), name="cms-pages-by-path"),
]

