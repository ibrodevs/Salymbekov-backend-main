from rest_framework import serializers
from .models import Category, News, Publication, PublicationCategory


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


class NewsSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "description",
            "short_description",
            "image",
            "is_recommended",
            "created_at",
            "updated_at",
            "published_at",
            "category",
            "is_banner",
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


class PublicationCategorySerializer(
    LocalizationSerializerMixin, serializers.ModelSerializer
):
    title = serializers.SerializerMethodField()

    class Meta:
        model = PublicationCategory
        fields = ["id", "title"]
        read_only_fields = ["id"]

    def get_title(self, obj):
        language = self._get_language()
        return obj.get_title(language=language)


class PublicationSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):
    category = PublicationCategorySerializer(read_only=True)
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = [
            "id",
            "title",
            "short_description",
            "description",
            "author",
            "pdf_file",
            "published_at",
            "created_at",
            "updated_at",
            "category",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_title(self, obj):
        return obj.get_title(language=self._get_language())

    def get_short_description(self, obj):
        return obj.get_short_description(language=self._get_language())

    def get_description(self, obj):
        return obj.get_description(language=self._get_language())
