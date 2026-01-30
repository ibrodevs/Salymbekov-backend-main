from django.shortcuts import render
from rest_framework import generics
from .serializers import PartnerSerializer
from .models import Partner

# Create your views here.

class PartnerListAPIView(generics.ListAPIView):
	serializer_class = PartnerSerializer
	queryset = Partner.objects.all()

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['language'] = self.request.query_params.get("lang", "ru")
		return context
