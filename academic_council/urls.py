from django.urls import path
from . import views

urlpatterns = [
    path('', views.AcademicCouncilView.as_view(), name='academic-council-list')
]