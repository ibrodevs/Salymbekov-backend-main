from .models import AcademicCouncil
from rest_framework import serializers

class AcademicCouncilSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = AcademicCouncil
        fields = ['name','photo', 'role', 'id']

    def get_name(self, obj):
        lang = self.context.get('lang', 'ru')
        return obj.get_name(lang=lang)

    def get_role(self, obj):
        lang = self.context.get('lang', 'ru')
        return obj.get_role(lang=lang)

