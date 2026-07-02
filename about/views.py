from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import NotFound
from .models import DevelopmentCouncilMember, PageContent, ScientificTechnicalCouncilMember
from .serializers import (
    DevelopmentCouncilSerializer,
    PageContentSerializer,
    ScientificTechnicalCouncilSerializer
)


class PageContentDetailView(RetrieveAPIView):
    serializer_class = PageContentSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return PageContent.objects.filter(is_active=True).prefetch_related('media')


class PageContentListView(ListAPIView):
    serializer_class = PageContentSerializer

    def get_queryset(self):
        return PageContent.objects.filter(is_active=True).prefetch_related('media')


class PageContentByPathView(RetrieveAPIView):
    serializer_class = PageContentSerializer

    def get_object(self):
        path = self.request.query_params.get('path', '')

        if not path:
            raise NotFound('Path is required')

        if not path.startswith('/'):
            path = f'/{path}'

        try:
            return PageContent.objects.prefetch_related('media').get(path=path, is_active=True)
        except PageContent.DoesNotExist:
            raise NotFound('Page content not found')


class DevelopmentCouncilListView(ListAPIView):
    serializer_class = DevelopmentCouncilSerializer

    def get_queryset(self):
        return DevelopmentCouncilMember.objects.filter(is_active=True)


class ScientificTechnicalCouncilListView(ListAPIView):
    serializer_class = ScientificTechnicalCouncilSerializer

    def get_queryset(self):
        return ScientificTechnicalCouncilMember.objects.filter(is_active=True)


# Create your views here.
