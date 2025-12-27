from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):

    title_en = models.CharField(max_length=255, verbose_name="Название (EN)")
    title_ru = models.CharField(max_length=255, verbose_name="Название (RU)")
    title_kg = models.CharField(max_length=255, verbose_name="Название (KG)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title_ru"]

    def __str__(self):
        return self.get_title()

    def get_title(self, language="ru"):
        field_name = f"title_{language}"
        value = getattr(self, field_name, None)

        if value and value.strip():
            return value.strip()

        if language != "ru" and self.title_ru and self.title_ru.strip():
            return self.title_ru.strip()

        if language != "en" and self.title_en and self.title_en.strip():
            return self.title_en.strip()

        return f"Category #{self.kg}"

    @property
    def title(self):
        return self.get_title(language="ru") or ""

    def clean(self):
        super().clean()
        if not any([self.title_ru, self.title_en, self.title_kg]):
            raise ValidationError("Необходимо заполнить хотя бы одно название")


class News(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news",
        verbose_name="Категория",
    )

    is_recommended = models.BooleanField(
        default=False,
        verbose_name="Рекомендуемая",
        db_index=True,
        help_text="Отображать в разделе рекомендованных новостей",
    )

    title_en = models.CharField(max_length=255, verbose_name="Заголовок (EN)")
    title_ru = models.CharField(max_length=255, verbose_name="Заголовок (RU)")
    title_kg = models.CharField(max_length=255, verbose_name="Заголовок (KG)")

    short_description_en = models.TextField(
        blank=True,
        verbose_name="Краткое описание (EN)",
    )
    short_description_ru = models.TextField(
        blank=True,
        verbose_name="Краткое описание (RU)",
    )
    short_description_kg = models.TextField(
        blank=True,
        verbose_name="Краткое описание (KG)",
    )

    description_en = models.TextField(blank=True, verbose_name="Описание (EN)")
    description_ru = models.TextField(blank=True, verbose_name="Описание (RU)")
    description_kg = models.TextField(blank=True, verbose_name="Описание (KG)")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    published_at = models.DateField(
        null=True, blank=True, verbose_name="Дата публикации", db_index=True
    )

    image = models.ImageField(
        upload_to="news/",
        null=True,
        blank=True,
        verbose_name="Изображение",
        help_text="Рекомендуемый размер: 1200x630px",
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"], name="news_created_idx"),
            models.Index(
                fields=["is_recommended", "-created_at"], name="news_recommended_idx"
            ),
            models.Index(fields=["category", "-created_at"], name="news_category_idx"),
        ]

    def __str__(self):
        return self.get_title()

    def get_title(self, language="ru"):
        field_name = f"title_{language}"
        value = getattr(self, field_name, None)

        if value and value.strip():
            return value.strip()

        if language != "ru" and self.title_ru and self.title_ru.strip():
            return self.title_ru.strip()

        if language != "en" and self.title_en and self.title_en.strip():
            return self.title_en.strip()

        return f"News #{self.pk}" if self.pk else "New News"

    def get_description(self, language="ru"):
        field_name = f"description_{language}"
        value = getattr(self, field_name, None)

        if value and value.strip():
            return value.strip()

        if language != "ru" and self.description_ru and self.description_ru.strip():
            return self.description_ru.strip()

        if language != "en" and self.description_en and self.description_en.strip():
            return self.description_en.strip()

        return ""

    def get_short_description(self, language="ru"):
        field_name = f"short_description_{language}"
        value = getattr(self, field_name, None)

        if value and value.strip():
            return value.strip()

        if (
            language != "ru"
            and self.short_description_ru
            and self.short_description_ru.strip()
        ):
            return self.short_description_ru.strip()

        if (
            language != "en"
            and self.short_description_en
            and self.short_description_en.strip()
        ):
            return self.short_description_en.strip()

        return self.get_description(language)

    def clean(self):
        super().clean()
        if not any([self.title_ru, self.title_en, self.title_kg]):
            raise ValidationError("Необходимо заполнить хотя бы один заголовок")


class NewsImage(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name="gallery",
        verbose_name="Новость",
    )
    image = models.ImageField(
        upload_to="news/gallery/",
        verbose_name="Изображение",
        help_text="Изображение для галереи новости",
    )
    order = models.PositiveIntegerField(
        default=0, verbose_name="Порядок", help_text="Порядок отображения в галерее"
    )

    class Meta:
        verbose_name = "Изображение галереи новости"
        verbose_name_plural = "Изображения галереи новостей"
        ordering = ["order", "id"]

    def __str__(self):
        return f"Gallery image for {self.news.get_title()}"
