import os
import tempfile
from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from cms_pages.models import Page, PageLink, PageSection, PageCard
from cms_pages.university_update import apply_update, rewrite
from contact_pages.models import FooterSettings, FooterLink
from about.models import PageContent


class UniversityUpdateTests(TestCase):
    def test_archive_and_rename_keep_documents_and_history(self):
        old = Page.objects.create(path='/education/postgrad/test', admin_title='Archive', body_ru='Original')
        campus = Page.objects.create(path='/education/center', admin_title='Центр Нарына', title_en='Education and Innovation Center in Naryn', body_ru='<p>Центр Нарына — Высшая школа медицины</p>', data={'card': {'title_ru':'Высшая школа медицины'}})
        card = PageCard.objects.create(page=campus, title_ru='Последипломное образование')
        link = PageLink.objects.create(page=campus, url='/education/postgrad/phd', title_ru='PhD')
        legacy = PageContent.objects.create(slug='old-postgrad-test', path='/education/postgrad/test', body_ru='Legacy')
        footer, _ = FooterSettings.objects.get_or_create(key='main')
        footerlink = FooterLink.objects.create(footer=footer, section='academic', url='/education/postgrad', title_ru='Последипломное образование')
        apply_update()
        for obj in (old,campus,link,legacy,footerlink,card): obj.refresh_from_db()
        self.assertFalse(old.is_published)
        self.assertEqual(old.body_ru, 'Original')
        self.assertFalse(legacy.is_active)
        self.assertFalse(link.is_active)
        self.assertFalse(card.is_active)
        self.assertTrue(PageCard.objects.filter(pk=card.pk).exists())
        self.assertFalse(footerlink.is_active)
        self.assertEqual(campus.admin_title, 'Нарын кампус')
        self.assertEqual(campus.title_en, 'Naryn Campus')
        self.assertEqual(campus.body_ru, '<p>Нарын кампус — ИГН</p>')
        self.assertEqual(campus.data['card']['title_ru'], 'ИГН')
        self.assertEqual(rewrite('Международный факультет медицины'), 'Международный факультет медицины')
        self.assertEqual(rewrite('Higher School of Medicine at Nazarbayev University'), 'Higher School of Medicine at Nazarbayev University')

    def test_pages_localization_sections_and_idempotence(self):
        apply_update()
        count = PageSection.objects.count()
        apply_update()
        self.assertEqual(PageSection.objects.count(), count)
        for path in ['/education','/education/student','/education/applicant']:
            page = Page.objects.get(path=path)
            for lang in ['ru','en','kg']:
                response = self.client.get('/api/pages/by-path/', {'path':path,'lang':lang})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()['title'], getattr(page, 'title_'+lang))
                self.assertGreater(len(response.json()['data']['sections']), 0)
                self.assertTrue(response.json()['seo_title'])
            self.assertFalse(page.show_media_gallery)

    def test_dry_run_rolls_back_and_backup_required_for_apply(self):
        from django.core.management.base import CommandError
        Page.objects.filter(path='/education/student').delete()
        call_command('update_university_2026', stdout=StringIO())
        self.assertFalse(Page.objects.filter(path='/education/student').exists())
        with self.assertRaises(CommandError):
            call_command('update_university_2026', apply=True)
        with tempfile.TemporaryDirectory() as directory:
            target = os.path.join(directory, 'backup.json')
            call_command('update_university_2026', apply=True, backup=target, stdout=StringIO())
            self.assertEqual(os.stat(target).st_mode & 0o777, 0o600)
            self.assertTrue(Page.objects.filter(path='/education/student').exists())
            with self.assertRaises(CommandError):
                call_command('update_university_2026', apply=True, backup=target)

    def test_retired_pages_are_never_public_even_if_republished(self):
        Page.objects.create(path='/education/postgrad/reopened', admin_title='Old', is_published=True)
        self.assertEqual(self.client.get('/api/pages/by-path/', {'path':'/education/postgrad/reopened'}).status_code, 404)
        self.assertNotIn('/education/postgrad/reopened', str(self.client.get('/api/pages/').json()))

    def test_database_backup_preserves_original_and_is_not_public(self):
        import json
        from cms_pages.models import ContentSnapshot
        original = Page.objects.create(path='/snapshot-test', admin_title='Центр Нарына', body_ru='Оригинальный текст')
        call_command('update_university_2026', apply=True, database_backup=True, stdout=StringIO())
        original.refresh_from_db()
        self.assertEqual(original.admin_title, 'Нарын кампус')
        snapshot = ContentSnapshot.objects.latest('created_at')
        record = next(row for row in json.loads(snapshot.payload) if row['model']=='cms_pages.page' and row['pk']==original.pk)
        self.assertEqual(record['fields']['admin_title'], 'Центр Нарына')
        self.assertEqual(record['fields']['body_ru'], 'Оригинальный текст')
        self.assertNotIn('payload', str(self.client.get('/api/pages/').json()))
        call_command('update_university_2026', apply=True, database_backup=True, stdout=StringIO())
        count = ContentSnapshot.objects.count()
        call_command('update_university_2026', apply=True, database_backup=True, stdout=StringIO())
        self.assertEqual(ContentSnapshot.objects.count(), count)

    def test_failed_update_rolls_back_original_content(self):
        from unittest.mock import patch
        from cms_pages.models import ContentSnapshot
        original = Page.objects.create(path='/rollback-test', admin_title='Before')
        count = ContentSnapshot.objects.count()
        def fail_after_write():
            Page.objects.filter(pk=original.pk).update(admin_title='Partial update')
            raise RuntimeError('abort update')
        with patch('cms_pages.management.commands.update_university_2026.apply_update', side_effect=fail_after_write):
            with self.assertRaises(RuntimeError):
                call_command('update_university_2026', apply=True, database_backup=True, stdout=StringIO())
        original.refresh_from_db()
        self.assertEqual(original.admin_title, 'Before')
        self.assertEqual(ContentSnapshot.objects.count(), count)
