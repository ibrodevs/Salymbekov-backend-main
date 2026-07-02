from django.urls import path
from .views import (
    DevelopmentCouncilListView,
    PageContentByPathView,
    PageContentDetailView,
    PageContentListView,
    ScientificTechnicalCouncilListView
)

urlpatterns = [
    path('pages/', PageContentListView.as_view()),
    path('pages/by-path/', PageContentByPathView.as_view()),
    path('pages/<slug:slug>/', PageContentDetailView.as_view()),
    path('development-council/', DevelopmentCouncilListView.as_view()),
    path('scientific-technical-council/', ScientificTechnicalCouncilListView.as_view()),
]
