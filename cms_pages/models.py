from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


LANGUAGE_CHOICES = (
    ("ru", "Русский"),
    ("en", "English"),
    ("kg", "Кыргызча"),
)


def normalize_path(value):
    if not value:
        return "/"

    normalized = value.strip()

    if not normalized.startswith("/"):
        normalized = f"/{normalized}"

    if len(normalized) > 1 and normalized.endswith("/"):
        normalized = normalized.rstrip("/")

    return normalized or "/"


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        abstract = True


class Page(TimeStampedModel):
    TEMPLATE_DEFAULT = "default"
    TEMPLATE_LANDING = "landing"
    TEMPLATE_DOCUMENTS = "documents"
    TEMPLATE_CHOICES = (
        (TEMPLATE_DEFAULT, "Универсальный"),
        (TEMPLATE_LANDING, "Лендинг"),
        (TEMPLATE_DOCUMENTS, "Документы"),
    )

    admin_title = models.CharField("Название в админке", max_length=255)
    path = models.CharField("Путь страницы", max_length=255, unique=True)
    navigation_group = models.CharField("Раздел", max_length=120, blank=True)
    template = models.CharField(
        "Шаблон",
        max_length=32,
        choices=TEMPLATE_CHOICES,
        default=TEMPLATE_DEFAULT,
    )

    title_ru = models.CharField("Заголовок (рус)", max_length=255, blank=True)
    title_en = models.CharField("Title (eng)", max_length=255, blank=True)
    title_kg = models.CharField("Аталышы (кр)", max_length=255, blank=True)

    subtitle_ru = models.TextField("Подзаголовок (рус)", blank=True)
    subtitle_en = models.TextField("Subtitle (eng)", blank=True)
    subtitle_kg = models.TextField("Кошумча аталыш (кр)", blank=True)

    body_ru = CKEditor5Field("Основной текст (рус)", blank=True, config_name="extends")
    body_en = CKEditor5Field("Main text (eng)", blank=True, config_name="extends")
    body_kg = CKEditor5Field("Негизги текст (кр)", blank=True, config_name="extends")

    seo_title_ru = models.CharField("SEO title (рус)", max_length=255, blank=True)
    seo_title_en = models.CharField("SEO title (eng)", max_length=255, blank=True)
    seo_title_kg = models.CharField("SEO title (кр)", max_length=255, blank=True)

    seo_description_ru = models.TextField("SEO description (рус)", blank=True)
    seo_description_en = models.TextField("SEO description (eng)", blank=True)
    seo_description_kg = models.TextField("SEO description (кр)", blank=True)

    data = models.JSONField(
        "Дополнительные данные",
        default=dict,
        blank=True,
        help_text="Для нестандартных блоков страницы. Обычные тексты, медиа, документы и ссылки лучше хранить в отдельных секциях ниже.",
    )
    internal_notes = models.TextField(
        "Внутренние заметки",
        blank=True,
        help_text="Технические заметки для контент-менеджеров. На frontend не выводится.",
    )
    force_backend_render = models.BooleanField(
        "Всегда рендерить из CMS",
        default=False,
        help_text="Если включено, frontend будет использовать CMS-страницу даже при минимальном наполнении.",
    )
    is_published = models.BooleanField("Опубликовано", default=True)

    class Meta:
        ordering = ["navigation_group", "admin_title", "path"]
        verbose_name = "CMS страница"
        verbose_name_plural = "CMS страницы"

    def __str__(self):
        return f"{self.admin_title} ({self.path})"

    def save(self, *args, **kwargs):
        self.path = normalize_path(self.path)
        super().save(*args, **kwargs)

    @property
    def has_meaningful_content(self):
        text_fields = [
            self.title_ru,
            self.title_en,
            self.title_kg,
            self.subtitle_ru,
            self.subtitle_en,
            self.subtitle_kg,
            self.body_ru,
            self.body_en,
            self.body_kg,
        ]
        return any(text_fields) or any(
            [
                self.force_backend_render,
                self.sections.exists(),
                self.cards.exists(),
                self.stats.exists(),
                self.media_items.exists(),
                self.documents.exists(),
                self.links.exists(),
                bool(self.data),
            ]
        )


class OrderedPageItem(TimeStampedModel):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class PageSection(OrderedPageItem):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="sections")

    title_ru = models.CharField("Заголовок (рус)", max_length=255, blank=True)
    title_en = models.CharField("Title (eng)", max_length=255, blank=True)
    title_kg = models.CharField("Аталышы (кр)", max_length=255, blank=True)

    subtitle_ru = models.TextField("Подзаголовок (рус)", blank=True)
    subtitle_en = models.TextField("Subtitle (eng)", blank=True)
    subtitle_kg = models.TextField("Кошумча аталыш (кр)", blank=True)

    body_ru = CKEditor5Field("Текст (рус)", blank=True, config_name="extends")
    body_en = CKEditor5Field("Text (eng)", blank=True, config_name="extends")
    body_kg = CKEditor5Field("Текст (кр)", blank=True, config_name="extends")

    class Meta(OrderedPageItem.Meta):
        verbose_name = "Секция страницы"
        verbose_name_plural = "Секции страницы"

    def __str__(self):
        return self.title_ru or self.title_en or self.title_kg or f"Секция #{self.pk}"


class PageCard(OrderedPageItem):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="cards")

    title_ru = models.CharField("Заголовок (рус)", max_length=255, blank=True)
    title_en = models.CharField("Title (eng)", max_length=255, blank=True)
    title_kg = models.CharField("Аталышы (кр)", max_length=255, blank=True)

    text_ru = models.TextField("Текст (рус)", blank=True)
    text_en = models.TextField("Text (eng)", blank=True)
    text_kg = models.TextField("Текст (кр)", blank=True)

    class Meta(OrderedPageItem.Meta):
        verbose_name = "Карточка страницы"
        verbose_name_plural = "Карточки страницы"

    def __str__(self):
        return self.title_ru or self.title_en or self.title_kg or f"Карточка #{self.pk}"


class PageStat(OrderedPageItem):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="stats")

    label_ru = models.CharField("Подпись (рус)", max_length=255, blank=True)
    label_en = models.CharField("Label (eng)", max_length=255, blank=True)
    label_kg = models.CharField("Жазуу (кр)", max_length=255, blank=True)

    value = models.CharField("Значение", max_length=255)

    description_ru = models.TextField("Описание (рус)", blank=True)
    description_en = models.TextField("Description (eng)", blank=True)
    description_kg = models.TextField("Сүрөттөмө (кр)", blank=True)

    class Meta(OrderedPageItem.Meta):
        verbose_name = "Показатель страницы"
        verbose_name_plural = "Показатели страницы"

    def __str__(self):
        return f"{self.value} - {self.label_ru or self.label_en or self.label_kg or 'Без подписи'}"


class PageMedia(OrderedPageItem):
    TYPE_IMAGE = "image"
    TYPE_FILE = "file"
    TYPE_VIDEO = "video"
    MEDIA_TYPE_CHOICES = (
        (TYPE_IMAGE, "Изображение"),
        (TYPE_FILE, "Файл"),
        (TYPE_VIDEO, "Видео/ссылка"),
    )

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="media_items")
    media_type = models.CharField("Тип", max_length=16, choices=MEDIA_TYPE_CHOICES, default=TYPE_IMAGE)
    file = models.FileField("Загруженный файл", upload_to="cms/pages/media/", blank=True, null=True)
    external_url = models.URLField("Внешняя ссылка", blank=True)
    is_hero = models.BooleanField("Hero медиа", default=False)

    title_ru = models.CharField("Название (рус)", max_length=255, blank=True)
    title_en = models.CharField("Title (eng)", max_length=255, blank=True)
    title_kg = models.CharField("Аталышы (кр)", max_length=255, blank=True)

    alt_text_ru = models.CharField("Alt текст (рус)", max_length=255, blank=True)
    alt_text_en = models.CharField("Alt text (eng)", max_length=255, blank=True)
    alt_text_kg = models.CharField("Alt текст (кр)", max_length=255, blank=True)

    class Meta(OrderedPageItem.Meta):
        verbose_name = "Медиа страницы"
        verbose_name_plural = "Медиа страницы"

    def __str__(self):
        return self.title_ru or self.title_en or self.title_kg or self.external_url or f"Медиа #{self.pk}"

    @property
    def resolved_url(self):
        if self.file:
            return self.file.url
        return self.external_url


class PageDocument(OrderedPageItem):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField("Файл", upload_to="cms/pages/documents/", blank=True, null=True)
    external_url = models.URLField("Внешняя ссылка", blank=True)

    title_ru = models.CharField("Название (рус)", max_length=255, blank=True)
    title_en = models.CharField("Title (eng)", max_length=255, blank=True)
    title_kg = models.CharField("Аталышы (кр)", max_length=255, blank=True)

    class Meta(OrderedPageItem.Meta):
        verbose_name = "Документ страницы"
        verbose_name_plural = "Документы страницы"

    def __str__(self):
        return self.title_ru or self.title_en or self.title_kg or self.external_url or f"Документ #{self.pk}"

    @property
    def resolved_url(self):
        if self.file:
            return self.file.url
        return self.external_url


class PageLink(OrderedPageItem):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="links")
    url = models.URLField("Ссылка")
    external = models.BooleanField("Открывать в новой вкладке", default=True)

    title_ru = models.CharField("Название (рус)", max_length=255, blank=True)
    title_en = models.CharField("Title (eng)", max_length=255, blank=True)
    title_kg = models.CharField("Аталышы (кр)", max_length=255, blank=True)

    class Meta(OrderedPageItem.Meta):
        verbose_name = "Ссылка страницы"
        verbose_name_plural = "Ссылки страницы"

    def __str__(self):
        return self.title_ru or self.title_en or self.title_kg or self.url
