from rest_framework import serializers

from cms_pages.serializers import resolve_language, translated_value

from .models import FooterLink, FooterSettings


class LocalizedSerializerMixin:
    def get_lang(self):
        return resolve_language(self.context.get("request"))


class FooterLinkSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = FooterLink
        fields = ["id", "section", "title", "url", "icon", "order"]

    def get_title(self, obj):
        return translated_value(obj, "title", self.get_lang())


class FooterSettingsSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    quick_links_title = serializers.SerializerMethodField()
    academic_title = serializers.SerializerMethodField()
    social_title = serializers.SerializerMethodField()
    copyright = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = FooterSettings
        fields = [
            "id",
            "brand",
            "description",
            "address",
            "phone",
            "email",
            "website",
            "quick_links_title",
            "academic_title",
            "social_title",
            "copyright",
            "links",
            "updated_at",
        ]

    def get_brand(self, obj):
        return translated_value(obj, "brand", self.get_lang())

    def get_description(self, obj):
        return translated_value(obj, "description", self.get_lang())

    def get_address(self, obj):
        return translated_value(obj, "address", self.get_lang())

    def get_quick_links_title(self, obj):
        return translated_value(obj, "quick_links_title", self.get_lang())

    def get_academic_title(self, obj):
        return translated_value(obj, "academic_title", self.get_lang())

    def get_social_title(self, obj):
        return translated_value(obj, "social_title", self.get_lang())

    def get_copyright(self, obj):
        return translated_value(obj, "copyright", self.get_lang())

    def get_links(self, obj):
        queryset = obj.links.filter(is_active=True).order_by("section", "order", "id")
        return FooterLinkSerializer(queryset, many=True, context=self.context).data
