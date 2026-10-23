from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .management.commands.bootstrap_site_pages import collect_cms_routes
from .models import Page, PageDocument, PageLink, PageMedia, PageSection, normalize_path


class CmsPagesTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(
            admin_title="About",
            path="about/",
            title_ru="О нас",
            title_en="About us",
            title_kg="Биз жөнүндө",
            subtitle_ru="Короткое описание",
            subtitle_en="Short description",
            subtitle_kg="Кыскача сүрөттөмө",
            body_ru="<p>Основной текст</p>",
            body_en="<p>Main text</p>",
            body_kg="<p>Негизги текст</p>",
            force_backend_render=True,
            data={
                "badge": {
                    "ru": "Университет",
                    "en": "University",
                    "kg": "Университет",
                },
                "hero": {
                    "button_ru": "Подробнее",
                    "button_en": "Learn more",
                    "button_kg": "Кененирээк",
                    "items": [
                        {
                            "label": {
                                "ru": "Обучение",
                                "en": "Education",
                                "kg": "Билим берүү",
                            }
                        }
                    ],
                },
                "show_block": True,
            },
        )
        PageSection.objects.create(
            page=self.page,
            title_ru="Секция",
            title_en="Section",
            title_kg="Бөлүм",
            body_ru="<p>Текст секции</p>",
            body_en="<p>Section text</p>",
            body_kg="<p>Бөлүмдүн тексти</p>",
            order=1,
        )
        PageMedia.objects.create(page=self.page, external_url="https://example.com/hero.jpg", is_hero=True, order=1)
        PageDocument.objects.create(
            page=self.page,
            external_url="https://example.com/file.pdf",
            title_ru="Файл",
            title_en="File",
            title_kg="Файл",
            order=1,
        )
        PageLink.objects.create(
            page=self.page,
            url="https://example.com",
            title_ru="Ссылка",
            title_en="Link",
            title_kg="Шилтеме",
            order=1,
        )

    def test_normalize_path(self):
        self.assertEqual(normalize_path("about/"), "/about")
        self.assertEqual(normalize_path("/about/"), "/about")

    def test_page_by_path_endpoint(self):
        response = self.client.get(reverse("cms-pages-by-path"), {"path": "about", "lang": "ru"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["path"], "/about")
        self.assertEqual(payload["title"], "О нас")
        self.assertEqual(payload["data"]["hero_image"], "https://example.com/hero.jpg")
        self.assertEqual(payload["data"]["documents"][0]["title"], "Файл")
        self.assertEqual(payload["data"]["links"][0]["title"], "Ссылка")

    def test_nested_page_data_is_localized_in_english(self):
        response = self.client.get(reverse("cms-pages-by-path"), {"path": "about", "lang": "en"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["title"], "About us")
        self.assertEqual(payload["subtitle"], "Short description")
        self.assertEqual(payload["body"], "<p>Main text</p>")
        self.assertEqual(payload["data"]["badge"], "University")
        self.assertEqual(payload["data"]["hero"]["button"], "Learn more")
        self.assertEqual(payload["data"]["hero"]["items"][0]["label"], "Education")
        self.assertEqual(payload["data"]["sections"][0]["title"], "Section")
        self.assertEqual(payload["data"]["documents"][0]["title"], "File")
        self.assertEqual(payload["data"]["links"][0]["title"], "Link")
        self.assertTrue(payload["data"]["show_block"])

    def test_nested_page_data_is_localized_in_kyrgyz(self):
        response = self.client.get(reverse("cms-pages-by-path"), {"path": "about", "lang": "ky"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["title"], "Биз жөнүндө")
        self.assertEqual(payload["subtitle"], "Кыскача сүрөттөмө")
        self.assertEqual(payload["body"], "<p>Негизги текст</p>")
        self.assertEqual(payload["data"]["hero"]["button"], "Кененирээк")
        self.assertEqual(payload["data"]["hero"]["items"][0]["label"], "Билим берүү")
        self.assertEqual(payload["data"]["sections"][0]["title"], "Бөлүм")
        self.assertEqual(payload["data"]["links"][0]["title"], "Шилтеме")

    def test_missing_translation_does_not_mix_russian_body_into_english(self):
        self.page.body_en = ""
        self.page.save(update_fields=["body_en", "updated_at"])

        response = self.client.get(reverse("cms-pages-by-path"), {"path": "about", "lang": "en"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["title"], "About us")
        self.assertEqual(payload["body"], "")
        self.assertNotIn("Основной текст", payload["body"])


class BootstrapRouteParsingTests(SimpleTestCase):
    def test_collects_managed_cms_only_and_home_routes(self):
        source = """
        <Route path="/" element={<HomeCmsPage isSplashVisible={false} />} />
        <Route path="/about" element={cmsOnlyPage('/about')} />
        <Route path="/legacy" element={managedPage('/legacy', <LegacyPage />)} />
        """
        routes = {route["path"]: route for route in collect_cms_routes(source)}

        self.assertEqual(set(routes), {"/", "/about", "/legacy"})
        self.assertEqual(routes["/"]["mode"], "cms-only")
        self.assertEqual(routes["/about"]["mode"], "cms-only")
        self.assertEqual(routes["/legacy"]["mode"], "managed")
        self.assertEqual(routes["/legacy"]["component"], "LegacyPage")
