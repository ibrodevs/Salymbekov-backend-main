from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Category, News
from .serializers import (
    CategorySerializer,
    NewsSerializer,
)


class LocalizationMixin:

    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = (
            self.request.GET.get("lang")
            or getattr(self.request, "LANGUAGE_CODE", None)
            or "ru"
        )
        context.update({"language": language})
        return context


class CategoryViewSet(LocalizationMixin, ReadOnlyModelViewSet):

    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title_en", "title_ru", "title_kg", "slug"]
    ordering_fields = ["id", "title_ru", "title_en", "title_kg"]


class NewsViewSet(LocalizationMixin, ReadOnlyModelViewSet):

    queryset = News.objects.select_related("category").prefetch_related("gallery").all().order_by("-created_at")
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "is_recommended"]
    search_fields = [
        "title_en",
        "title_ru",
        "title_kg",
        "description_en",
        "description_ru",
        "description_kg",
    ]
    ordering_fields = ["created_at", "is_recommended", "title_ru"]

    @action(detail=False, methods=["get"])
    def recommended(self, request):

        recommended_news = self.queryset.filter(is_recommended=True)
        page = self.paginate_queryset(recommended_news)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recommended_news, many=True)
        return Response(serializer.data)
