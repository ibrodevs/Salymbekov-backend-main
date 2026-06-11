from rest_framework import serializers
from .models import (
    DevelopmentCouncilMember,
    PageContent,
    PageMedia,
    ScientificTechnicalCouncilMember,
)


def get_request_language(context):
    request = context.get('request')
    if not request:
        return 'ru'

    lang = request.query_params.get('lang', 'ru')
    if lang not in ['ru', 'en', 'kg']:
        return 'ru'

    return lang


class PageMediaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = PageMedia
        fields = [
            'id',
            'key',
            'title',
            'media_type',
            'url',
            'order',
        ]

    def get_url(self, obj):
        if obj.external_url:
            return obj.external_url

        if not obj.file:
            return ''

        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)

        return obj.file.url


class PageContentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subtitle = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    class Meta:
        model = PageContent
        fields = [
            'id',
            'slug',
            'path',
            'title',
            'subtitle',
            'body',
            'data',
            'media',
            'updated_at',
        ]

    def get_title(self, obj):
        lang = get_request_language(self.context)
        return getattr(obj, f'title_{lang}', obj.title_ru) or obj.title_ru

    def get_subtitle(self, obj):
        lang = get_request_language(self.context)
        return getattr(obj, f'subtitle_{lang}', obj.subtitle_ru) or obj.subtitle_ru

    def get_body(self, obj):
        lang = get_request_language(self.context)
        return getattr(obj, f'body_{lang}', obj.body_ru) or obj.body_ru

    def get_media(self, obj):
        media = obj.media.filter(is_active=True)
        return PageMediaSerializer(media, many=True, context=self.context).data


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
        return get_request_language(self.context)

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
        return get_request_language(self.context)

    def get_full_name(self, obj):
        lang = self.get_language()
        return getattr(obj, f'full_name_{lang}', obj.full_name_ru)

    def get_role(self, obj):
        lang = self.get_language()
        return getattr(obj, f'role_{lang}', obj.role_ru)
