from django.urls import path
from .views import (
    DevelopmentCouncilListView,
    ScientificTechnicalCouncilListView
)

urlpatterns = [
    path('development-council/', DevelopmentCouncilListView.as_view()),
    path('scientific-technical-council/', ScientificTechnicalCouncilListView.as_view()),
]
