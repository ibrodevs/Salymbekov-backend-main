from rest_framework import serializers

from .models import Page, PageCard, PageDocument, PageLink, PageMedia, PageSection, PageStat


SUPPORTED_LANGUAGES = {"ru", "en", "kg"}


def resolve_language(request):
    if not request:
        return "ru"

    params = getattr(request, "query_params", None)
    if params is None:
        params = getattr(request, "GET", {})

    lang = params.get("lang", "ru").lower()
    return lang if lang in SUPPORTED_LANGUAGES else "ru"


def translated_value(obj, base_name, lang):
    candidates = [lang, "ru", "en", "kg"]

    for suffix in candidates:
        value = getattr(obj, f"{base_name}_{suffix}", "")
        if value:
            return value

    return ""


class LocalizedSerializerMixin:
    def get_lang(self):
        return resolve_language(self.context.get("request"))


class PageSectionSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subtitle = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    class Meta:
        model = PageSection
        fields = ["id", "title", "subtitle", "body", "order"]

    def get_title(self, obj):
        return translated_value(obj, "title", self.get_lang())

    def get_subtitle(self, obj):
        return translated_value(obj, "subtitle", self.get_lang())

    def get_body(self, obj):
        return translated_value(obj, "body", self.get_lang())


class PageCardSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = PageCard
        fields = ["id", "title", "text", "order"]

    def get_title(self, obj):
        return translated_value(obj, "title", self.get_lang())

    def get_text(self, obj):
        return translated_value(obj, "text", self.get_lang())


class PageStatSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = PageStat
        fields = ["id", "label", "value", "description", "order"]

    def get_label(self, obj):
        return translated_value(obj, "label", self.get_lang())

    def get_description(self, obj):
        return translated_value(obj, "description", self.get_lang())


class PageMediaSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    alt_text = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = PageMedia
        fields = ["id", "title", "alt_text", "url", "media_type", "is_hero", "order"]

    def get_title(self, obj):
        return translated_value(obj, "title", self.get_lang())

    def get_alt_text(self, obj):
        return translated_value(obj, "alt_text", self.get_lang())

    def get_url(self, obj):
        return obj.resolved_url


class PageDocumentSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = PageDocument
        fields = ["id", "title", "url", "order"]

    def get_title(self, obj):
        return translated_value(obj, "title", self.get_lang())

    def get_url(self, obj):
        return obj.resolved_url


class PageLinkSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = PageLink
        fields = ["id", "title", "url", "external", "order"]

    def get_title(self, obj):
        return translated_value(obj, "title", self.get_lang())


class PageDetailSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subtitle = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    seo_title = serializers.SerializerMethodField()
    seo_description = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = [
            "id",
            "admin_title",
            "path",
            "template",
            "title",
            "subtitle",
            "body",
            "seo_title",
            "seo_description",
            "force_backend_render",
            "media",
            "documents",
            "links",
            "data",
            "updated_at",
        ]

    def get_title(self, obj):
        return translated_value(obj, "title", self.get_lang())

    def get_subtitle(self, obj):
        return translated_value(obj, "subtitle", self.get_lang())

    def get_body(self, obj):
        return translated_value(obj, "body", self.get_lang())

    def get_seo_title(self, obj):
        return translated_value(obj, "seo_title", self.get_lang())

    def get_seo_description(self, obj):
        return translated_value(obj, "seo_description", self.get_lang())

    def get_media(self, obj):
        return PageMediaSerializer(obj.media_items.all(), many=True, context=self.context).data

    def get_documents(self, obj):
        return PageDocumentSerializer(obj.documents.all(), many=True, context=self.context).data

    def get_links(self, obj):
        return PageLinkSerializer(obj.links.all(), many=True, context=self.context).data

    def get_data(self, obj):
        payload = dict(obj.data or {})
        media_items = obj.media_items.all()
        hero_item = next((item for item in media_items if item.is_hero and item.resolved_url), None)
        fallback_hero = next((item for item in media_items if item.media_type == PageMedia.TYPE_IMAGE and item.resolved_url), None)

        payload["force_backend_render"] = obj.force_backend_render
        payload["sections"] = PageSectionSerializer(obj.sections.all(), many=True, context=self.context).data
        payload["cards"] = PageCardSerializer(obj.cards.all(), many=True, context=self.context).data
        payload["stats"] = PageStatSerializer(obj.stats.all(), many=True, context=self.context).data
        payload["documents"] = self.get_documents(obj)
        payload["links"] = self.get_links(obj)
        payload["hero_image"] = (hero_item or fallback_hero).resolved_url if (hero_item or fallback_hero) else payload.get("hero_image")
        return payload
