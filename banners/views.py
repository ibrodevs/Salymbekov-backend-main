from django.shortcuts import render
from rest_framework import generics
from .serializers import BannerSerializer
from .models import Banner
# Create your views here.

class BannerView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer