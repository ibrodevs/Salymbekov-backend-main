"""Read-only audit of published CMS links, names and translations."""
import json
import re
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from cms_pages.models import Page
from cms_pages.university_update import is_retired, RENAMES


class Command(BaseCommand):
    help = 'Emit JSON findings for all published CMS pages; --strict fails on findings.'

    def add_arguments(self, parser):
        parser.add_argument('--strict', action='store_true')

    def handle(self, *args, **options):
        from django.core.management.base import CommandError
        pages = list(Page.objects.filter(is_published=True).prefetch_related('sections','links','cards','media_items'))
        known = {p.path for p in pages} | {'/press/news','/news','/404'}
        findings = []
        for page in pages:
            if is_retired(page.path):
                findings.append({'path': page.path, 'issue': 'retired_published'})
                continue
            for lang in ('ru','en','kg'):
                texts = [getattr(page, f'{base}_{lang}') for base in ('title','subtitle','body','seo_title','seo_description')]
                texts += [getattr(section, f'{base}_{lang}') for section in page.sections.all() if section.is_active for base in ('title','subtitle','body')]
                texts += [getattr(card, f'{base}_{lang}') for card in page.cards.all() if card.is_active for base in ('title','text')]
                texts += [getattr(media, f'{base}_{lang}') for media in page.media_items.all() for base in ('title','alt_text')]
                texts += [getattr(link, f'title_{lang}') for link in page.links.all() if link.is_active]
                texts.append(json.dumps(page.data, ensure_ascii=False))
                value = '\n'.join(texts)
                if not getattr(page, f'title_{lang}'):
                    findings.append({'path':page.path,'lang':lang,'issue':'missing_title'})
                if any(re.search(pattern, value, re.I) for pattern, _ in RENAMES) and not re.search(r'Nazarbayev|Назарбаев', value, re.I):
                    findings.append({'path':page.path,'lang':lang,'issue':'old_department_name'})
                soup = BeautifulSoup(value, 'html.parser')
                urls = [a['href'] for a in soup.find_all('a', href=True)] + [link.url for link in page.links.all() if link.is_active]
                for url in set(urls):
                    target = urlsplit(url)
                    path = unquote(target.path).rstrip('/') or '/'
                    if target.scheme or target.netloc or not url.startswith('/'):
                        continue
                    if is_retired(path):
                        issue = 'retired_link'
                    elif path not in known and not path.startswith(('/media/','/assets/','/press/news/')) and not re.search(r'\.[a-zA-Z0-9]{2,5}$',path):
                        issue = 'unknown_internal_route'
                    else:
                        continue
                    findings.append({'path':page.path,'lang':lang,'issue':issue,'target':path})
        self.stdout.write(json.dumps({'pages':len(pages),'findings':findings},ensure_ascii=False,indent=2))
        if options['strict'] and findings:
            raise CommandError(f'{len(findings)} findings require review')
