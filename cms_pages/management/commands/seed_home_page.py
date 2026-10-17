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
        "badge": {"ru": "Партнеры", "en": "Partners", "kg": "Өнөктөштөр"},
        "title": {"ru": "Наши партнеры", "en": "Our partners", "kg": "Биздин өнөктөштөр"},
        "subtitle": {
            "ru": "Мы сотрудничаем с ведущими организациями для достижения общих целей и развития региона",
            "en": "We collaborate with leading organizations to achieve shared goals and regional development",
            "kg": "Жалпы максаттарга жана аймактык өнүгүүгө жетүү үчүн алдыңкы уюмдар менен кызматташабыз",
        },
    },
    "video": {
        "platform_label": {"ru": "YouTube", "en": "YouTube", "kg": "YouTube"},
    },
}

HOME_BODY = {
    "ru": "Салымбеков Университет — образовательная, научная и клиническая среда для подготовки современных специалистов.",
    "en": "Salymbekov University is an educational, scientific and clinical environment for training modern professionals.",
    "kg": "Салымбеков Университети — заманбап адистерди даярдоочу билим берүү, илимий жана клиникалык чөйрө.",
}


class Command(BaseCommand):
    help = "Создает CMS-настройки главной страницы, не перезаписывая уже настроенную администратором главную."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Принудительно обновить настройки главной страницы.",
        )

    def handle(self, *args, **options):
        page, created = Page.objects.get_or_create(
            path="/",
            defaults={"admin_title": "Home", "navigation_group": "home"},
        )

        already_configured = page.data.get("render_mode") == "homepage"

        # Even an already configured homepage should have complete RU/EN/KG text
        # fields for API/audit consistency. Fill only blanks; never overwrite
        # administrator text unless --force is explicitly requested.
        body_changed = False
        for lang, value in HOME_BODY.items():
            field_name = f"body_{lang}"
            if options["force"] or not (getattr(page, field_name, "") or "").strip():
                setattr(page, field_name, value)
                body_changed = True

        if not created and already_configured and not options["force"]:
            if body_changed:
                page.save(update_fields=["body_ru", "body_en", "body_kg", "updated_at"])
            self.stdout.write(
                self.style.SUCCESS("Главная уже настроена через CMS; существующие настройки администратора сохранены.")
            )
            return

        page.admin_title = page.admin_title or "Home"
        page.navigation_group = page.navigation_group or "home"
        page.template = Page.TEMPLATE_LANDING
        page.force_backend_render = True
        page.is_published = True

        page.title_ru = page.title_ru or "Главная страница"
        page.title_en = page.title_en or "Home page"
        page.title_kg = page.title_kg or "Башкы бет"

        page.subtitle_ru = page.subtitle_ru or "Главная страница сайта управляется через CMS."
        page.subtitle_en = page.subtitle_en or "The main landing page is managed from the CMS."
        page.subtitle_kg = page.subtitle_kg or "Сайттын башкы бети CMS аркылуу башкарылат."

        page.seo_title_ru = page.seo_title_ru or "Салымбеков Университет"
        page.seo_title_en = page.seo_title_en or "Salymbekov University"
        page.seo_title_kg = page.seo_title_kg or "Салымбеков Университети"

        page.seo_description_ru = page.seo_description_ru or "Главная страница Салымбеков Университета."
        page.seo_description_en = page.seo_description_en or "Main landing page of Salymbekov University."
        page.seo_description_kg = page.seo_description_kg or "Салымбеков Университетинин башкы бети."

        page.data = {**HOME_PAGE_DATA, **(page.data or {}), "render_mode": "homepage"}
        if not page.internal_notes:
            page.internal_notes = (
                "Главная страница собирается из backend-настроек: баннеры, новости, партнеры, "
                "видео и встроенные CMS-блоки. Новости остаются отдельным живым блоком."
            )
        page.save()

        verb = "Создана" if created else "Настроена"
        self.stdout.write(self.style.SUCCESS(f"{verb} CMS-страница главной: {page.path}"))
