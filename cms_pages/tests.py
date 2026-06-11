from django.test import TestCase
from django.urls import reverse

from .models import Page, PageDocument, PageLink, PageMedia, PageSection, normalize_path


class CmsPagesTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(
            admin_title="About",
            path="about/",
            title_ru="О нас",
            subtitle_ru="Короткое описание",
            body_ru="<p>Основной текст</p>",
            force_backend_render=True,
        )
        PageSection.objects.create(page=self.page, title_ru="Секция", body_ru="<p>Текст секции</p>", order=1)
        PageMedia.objects.create(page=self.page, external_url="https://example.com/hero.jpg", is_hero=True, order=1)
        PageDocument.objects.create(page=self.page, external_url="https://example.com/file.pdf", title_ru="Файл", order=1)
        PageLink.objects.create(page=self.page, url="https://example.com", title_ru="Ссылка", order=1)

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

