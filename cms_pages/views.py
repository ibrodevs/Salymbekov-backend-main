from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Page, normalize_path
from .serializers import PageDetailSerializer


class PageByPathView(RetrieveAPIView):
    serializer_class = PageDetailSerializer

    def get_object(self):
        raw_path = self.request.query_params.get("path", "/")
        path = normalize_path(raw_path)

        queryset = (
            Page.objects.filter(is_published=True)
            .prefetch_related("sections", "cards", "stats", "media_items", "documents", "links")
        )
        return get_object_or_404(queryset, path=path)


class PageListView(ListAPIView):
    serializer_class = PageDetailSerializer

    def get_queryset(self):
        return (
            Page.objects.filter(is_published=True)
            .prefetch_related("sections", "cards", "stats", "media_items", "documents", "links")
            .order_by("navigation_group", "admin_title", "path")
        )

