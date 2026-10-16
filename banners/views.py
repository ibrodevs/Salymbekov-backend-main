from rest_framework import generics

from .models import Banner
from .serializers import BannerSerializer


class BannerView(generics.ListAPIView):
    queryset = Banner.objects.all().order_by("id")
    serializer_class = BannerSerializer
    pagination_class = None
