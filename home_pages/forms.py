from django import forms

from .models import HomePage


class HomePageAdminForm(forms.ModelForm):
    show_hero = forms.BooleanField(label="Показывать hero-баннер", required=False)
    show_news = forms.BooleanField(label="Показывать блок новостей", required=False)
    show_partners = forms.BooleanField(label="Показывать блок партнеров", required=False)
    show_video = forms.BooleanField(label="Показывать видео-блок", required=False)

    founder_page_path = forms.CharField(label="Путь блока учредителя", required=False)
    gallery_page_path = forms.CharField(label="Путь блока галереи", required=False)
    video_url = forms.URLField(label="URL видео", required=False)

    partners_badge_ru = forms.CharField(label="Бейдж партнеров (RU)", required=False)
    partners_badge_en = forms.CharField(label="Бейдж партнеров (EN)", required=False)
    partners_badge_kg = forms.CharField(label="Бейдж партнеров (KG)", required=False)

    partners_title_ru = forms.CharField(label="Заголовок партнеров (RU)", required=False)
    partners_title_en = forms.CharField(label="Заголовок партнеров (EN)", required=False)
    partners_title_kg = forms.CharField(label="Заголовок партнеров (KG)", required=False)

    partners_subtitle_ru = forms.CharField(
        label="Подзаголовок партнеров (RU)", required=False, widget=forms.Textarea(attrs={"rows": 3})
    )
    partners_subtitle_en = forms.CharField(
        label="Подзаголовок партнеров (EN)", required=False, widget=forms.Textarea(attrs={"rows": 3})
    )
    partners_subtitle_kg = forms.CharField(
        label="Подзаголовок партнеров (KG)", required=False, widget=forms.Textarea(attrs={"rows": 3})
    )

    video_platform_label_ru = forms.CharField(label="Подпись платформы видео (RU)", required=False)
    video_platform_label_en = forms.CharField(label="Подпись платформы видео (EN)", required=False)
    video_platform_label_kg = forms.CharField(label="Подпись платформы видео (KG)", required=False)

    class Meta:
        model = HomePage
        fields = [
            "admin_title",
            "path",
            "navigation_group",
            "template",
            "is_published",
            "force_backend_render",
            "title_ru",
            "title_en",
            "title_kg",
            "subtitle_ru",
            "subtitle_en",
            "subtitle_kg",
            "body_ru",
            "body_en",
            "body_kg",
            "seo_title_ru",
            "seo_title_en",
            "seo_title_kg",
            "seo_description_ru",
            "seo_description_en",
            "seo_description_kg",
            "internal_notes",
            "data",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = dict(self.instance.data or {})
        partners = data.get("partners") or {}
        video = data.get("video") or {}

        self.fields["show_hero"].initial = data.get("show_hero", True)
        self.fields["show_news"].initial = data.get("show_news", True)
        self.fields["show_partners"].initial = data.get("show_partners", True)
        self.fields["show_video"].initial = data.get("show_video", True)
        self.fields["founder_page_path"].initial = data.get("founder_page_path", "/founderMessege")
        self.fields["gallery_page_path"].initial = data.get("gallery_page_path", "/MaterialBaseGallery")
        self.fields["video_url"].initial = data.get("video_url", "")

        for lang in ("ru", "en", "kg"):
            self.fields[f"partners_badge_{lang}"].initial = (partners.get("badge") or {}).get(lang, "")
            self.fields[f"partners_title_{lang}"].initial = (partners.get("title") or {}).get(lang, "")
            self.fields[f"partners_subtitle_{lang}"].initial = (partners.get("subtitle") or {}).get(lang, "")
            self.fields[f"video_platform_label_{lang}"].initial = (video.get("platform_label") or {}).get(lang, "")

    def save(self, commit=True):
        instance = super().save(commit=False)
        data = dict(instance.data or {})

        data["render_mode"] = "homepage"
        data["show_hero"] = self.cleaned_data["show_hero"]
        data["show_news"] = self.cleaned_data["show_news"]
        data["show_partners"] = self.cleaned_data["show_partners"]
        data["show_video"] = self.cleaned_data["show_video"]
        data["founder_page_path"] = self.cleaned_data["founder_page_path"] or "/founderMessege"
        data["gallery_page_path"] = self.cleaned_data["gallery_page_path"] or "/MaterialBaseGallery"
        data["video_url"] = self.cleaned_data["video_url"] or ""

        data["partners"] = {
            "badge": {lang: self.cleaned_data[f"partners_badge_{lang}"] for lang in ("ru", "en", "kg")},
            "title": {lang: self.cleaned_data[f"partners_title_{lang}"] for lang in ("ru", "en", "kg")},
            "subtitle": {lang: self.cleaned_data[f"partners_subtitle_{lang}"] for lang in ("ru", "en", "kg")},
        }
        data["video"] = {
            "platform_label": {lang: self.cleaned_data[f"video_platform_label_{lang}"] for lang in ("ru", "en", "kg")}
        }

        instance.data = data

        if commit:
            instance.save()

        return instance
