from rest_framework import generics

from .models import Partner
from .serializers import PartnerSerializer


class PartnerListAPIView(generics.ListAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all().order_by("id")
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context
