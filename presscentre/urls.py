from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    NewsViewSet,
    BannerNewsViewSet,
    PublicationViewSet,
    PublicationCategoryViewSet,
)
from django.urls import path, include

app_name = "presscentre"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"news", NewsViewSet, basename="news")
router.register(r"publications", PublicationViewSet, basename="publication")
router.register(
    r"publication-categories",
    PublicationCategoryViewSet,
    basename="publication-category",
)

urlpatterns = [
    path("", include(router.urls)),
    path("news-banners/", BannerNewsViewSet.as_view(), name="banner-news"),
]
