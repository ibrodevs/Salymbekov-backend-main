from django.core.management.base import BaseCommand

from cms_pages.models import Page


HOME_PAGE_DATA = {
    "render_mode": "homepage",
    "show_hero": True,
    "show_news": True,
    "show_partners": True,
    "show_video": True,
    "founder_page_path": "/founderMessege",
    "gallery_page_path": "/MaterialBaseGallery",
    "video_url": "https://www.youtube.com/embed/SdluvCyzd6M",
    "partners": {
        "badge": {
            "ru": "Партнеры",
            "en": "Partners",
            "kg": "Өнөктөштөр",
        },
        "title": {
            "ru": "Наши партнеры",
            "en": "Our partners",
            "kg": "Биздин өнөктөштөр",
        },
        "subtitle": {
            "ru": "Мы сотрудничаем с ведущими организациями для достижения общих целей и развития региона",
            "en": "We collaborate with leading organizations to achieve shared goals and regional development",
            "kg": "Жалпы максаттарга жана аймактык өнүгүүгө жетүү үчүн алдыңкы уюмдар менен кызматташабыз",
        },
    },
    "video": {
        "platform_label": {
            "ru": "YouTube",
            "en": "YouTube",
            "kg": "YouTube",
        },
    },
}


class Command(BaseCommand):
    help = "Создает или обновляет CMS-страницу главной страницы."

    def handle(self, *args, **options):
        page, created = Page.objects.get_or_create(
            path="/",
            defaults={
                "admin_title": "Home",
                "navigation_group": "home",
            },
        )

        page.admin_title = "Home"
        page.navigation_group = "home"
        page.template = Page.TEMPLATE_LANDING
        page.force_backend_render = True
        page.is_published = True

        page.title_ru = "Главная страница"
        page.title_en = "Home page"
        page.title_kg = "Башкы бет"

        page.subtitle_ru = "Главная страница сайта управляется через CMS."
        page.subtitle_en = "The main landing page is managed from the CMS."
        page.subtitle_kg = "Сайттын башкы бети CMS аркылуу башкарылат."

        page.seo_title_ru = "Салымбеков Университет"
        page.seo_title_en = "Salymbekov University"
        page.seo_title_kg = "Салымбеков Университети"

        page.seo_description_ru = "Главная страница Салымбеков Университета."
        page.seo_description_en = "Main landing page of Salymbekov University."
        page.seo_description_kg = "Салымбеков Университетинин башкы бети."

        page.data = {
            **(page.data or {}),
            **HOME_PAGE_DATA,
        }
        page.internal_notes = (
            "Главная страница собирается из backend-настроек: баннеры, новости, партнеры, "
            "видео и встроенные CMS-блоки. Новости остаются отдельным живым блоком."
        )
        page.save()

        verb = "Создана" if created else "Обновлена"
        self.stdout.write(self.style.SUCCESS(f"{verb} CMS-страница главной: {page.path}"))
