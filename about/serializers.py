from rest_framework import serializers
from .models import DevelopmentCouncilMember, ScientificTechnicalCouncilMember


class DevelopmentCouncilSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = DevelopmentCouncilMember
        fields = [
            'id',
            'photo',
            'full_name',
            'role',
            'description',
            'is_council_member',
        ]

    def get_language(self):
        request = self.context.get('request')

        if not request:
            return 'ru'

        lang = request.query_params.get('lang', 'ru')

        if lang not in ['ru', 'en', 'kg']:
            lang = 'ru'

        return lang

    def get_full_name(self, obj):
        lang = self.get_language()
        return getattr(obj, f'full_name_{lang}', obj.full_name_ru)

    def get_role(self, obj):
        lang = self.get_language()
        return getattr(obj, f'role_{lang}', obj.role_ru)

    def get_description(self, obj):
        lang = self.get_language()
        return getattr(obj, f'description_{lang}', obj.description_ru)



class ScientificTechnicalCouncilSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = ScientificTechnicalCouncilMember
        fields = [
            'id',
            'full_name',
            'role',
            'is_head',
        ]

    def get_language(self):
        request = self.context.get('request')

        if not request:
            return 'ru'

        lang = request.query_params.get('lang', 'ru')

        if lang not in ['ru', 'en', 'kg']:
            lang = 'ru'

        return lang

    def get_full_name(self, obj):
        lang = self.get_language()
        return getattr(obj, f'full_name_{lang}', obj.full_name_ru)

    def get_role(self, obj):
        lang = self.get_language()
        return getattr(obj, f'role_{lang}', obj.role_ru)
