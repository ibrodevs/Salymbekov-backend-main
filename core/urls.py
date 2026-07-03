"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def api_root(request):
    return JsonResponse({
        "message": "Salymbekov University backend is running",
        "admin": "/admin/",
        "api": {
            "banners": "/api/banners/",
            "partners": "/api/partners/",
            "news": "/api/presscentre/news/",
            "pages": "/api/pages/",
            "page_by_path": "/api/pages/by-path/?path=/about",
            "page_content": "/api/pages/<slug>/",
        },
    })


urlpatterns = [
    path("", api_root),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("swagger", SpectacularSwaggerView.as_view(url_name="schema")),
    path("admin/", admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("api/presscentre/", include("presscentre.urls")),
    path('api/academic-council/', include('academic_council.urls')),
    path('api/banners/', include('banners.urls')),
    # Keep CMS routes before broader legacy "api/" includes to avoid accidental shadowing.
    path('api/', include('cms_pages.urls')),
    path('api/', include('partners.urls')),
    path('api/', include('about.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
