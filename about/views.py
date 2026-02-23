from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import DevelopmentCouncilMember, ScientificTechnicalCouncilMember
from .serializers import (
    DevelopmentCouncilSerializer,
    ScientificTechnicalCouncilSerializer
)


class DevelopmentCouncilListView(ListAPIView):
    serializer_class = DevelopmentCouncilSerializer

    def get_queryset(self):
        return DevelopmentCouncilMember.objects.filter(is_active=True)


class ScientificTechnicalCouncilListView(ListAPIView):
    serializer_class = ScientificTechnicalCouncilSerializer

    def get_queryset(self):
        return ScientificTechnicalCouncilMember.objects.filter(is_active=True)


# Create your views here.
