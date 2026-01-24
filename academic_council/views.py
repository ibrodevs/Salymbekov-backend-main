from rest_framework import generics
from .models import AcademicCouncil
from .serializers import AcademicCouncilSerializer


class AcademicCouncilView(generics.ListAPIView):
    queryset = AcademicCouncil.objects.all()
    serializer_class = AcademicCouncilSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'ru')
        context['lang'] = lang
        return context