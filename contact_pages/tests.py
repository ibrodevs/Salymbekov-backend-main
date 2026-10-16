from django.test import TestCase
from django.urls import reverse

from .models import FooterLink, FooterSettings


class FooterApiTests(TestCase):
    def setUp(self):
        self.footer, _ = FooterSettings.objects.get_or_create(key="main")
        self.footer.brand_ru = "Бренд"
        self.footer.brand_en = "Brand"
        self.footer.brand_kg = "Бренд KG"
        self.footer.description_ru = "Описание"
        self.footer.description_en = "Description"
        self.footer.description_kg = "Сүрөттөмө"
        self.footer.address_ru = "Адрес"
        self.footer.address_en = "Address"
        self.footer.address_kg = "Дарек"
        self.footer.is_active = True
        self.footer.save()

        FooterLink.objects.filter(footer=self.footer).delete()
        FooterLink.objects.create(
            footer=self.footer,
            section=FooterLink.SECTION_QUICK,
            title_ru="Контакты",
            title_en="Contacts",
            title_kg="Байланыш",
            url="/contacts",
            order=1,
        )

    def test_footer_endpoint_localizes_content(self):
        response = self.client.get(reverse("site-footer"), {"lang": "en"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["brand"], "Brand")
        self.assertEqual(payload["description"], "Description")
        self.assertEqual(payload["address"], "Address")
        self.assertEqual(payload["links"][0]["title"], "Contacts")
        self.assertEqual(payload["links"][0]["url"], "/contacts")

    def test_inactive_footer_is_not_public(self):
        self.footer.is_active = False
        self.footer.save(update_fields=["is_active", "updated_at"])
        response = self.client.get(reverse("site-footer"), {"lang": "ru"})
        self.assertEqual(response.status_code, 404)
