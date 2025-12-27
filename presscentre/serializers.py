from rest_framework import serializers
from .models import Category, News, NewsImage


class LocalizationSerializerMixin:
    """Миксин для локализации сериализаторов"""

    def _get_language(self):
        lang = self.context.get("language")
        if lang:
            return lang
        request = self.context.get("request")
        if request:
            return (
                request.GET.get("lang")
                or getattr(request, "LANGUAGE_CODE", None)
                or "ru"
            )
        return "ru"


class CategorySerializer(LocalizationSerializerMixin, serializers.ModelSerializer):

    title = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "title"]
        read_only_fields = ["id"]

    def get_title(self, obj):
        language = self._get_language()
        return obj.get_title(language=language)


class NewsImageSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = NewsImage
        fields = ["id", "image", "order"]
        read_only_fields = ["id"]


class NewsSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    gallery = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "description",
            "short_description",
            "image",
            "gallery",
            "is_recommended",
            "created_at",
            "updated_at",
            "published_at",
            "category",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_title(self, obj):
        language = self._get_language()
        return obj.get_title(language=language)

    def get_description(self, obj):
        language = self._get_language()
        return obj.get_description(language=language)

    def get_short_description(self, obj):
        language = self._get_language()
        return obj.get_short_description(language=language)
