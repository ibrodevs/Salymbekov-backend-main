import mimetypes
import re
import time
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify
from django.utils.timezone import make_aware

from presscentre.models import Category, News, NewsImage


SOURCE_URL = "https://salymbekov.com/en/latest-news/"
POSTS_URL = "https://salymbekov.com/wp-json/wp/v2/posts"
REQUEST_TIMEOUT = 30
USER_AGENT = "salymbekov-news-importer/1.0"


class ContentParser(HTMLParser):
    image_attrs = ("data-src", "data-lazy-src", "data-original", "src")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text_parts = []
        self.image_urls = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
            return

        if tag == "img":
            for attr_name in self.image_attrs:
                image_url = attrs_dict.get(attr_name)
                if image_url:
                    self.image_urls.append(image_url)
                    break

            srcset = attrs_dict.get("data-srcset") or attrs_dict.get("srcset")
            if srcset:
                first_src = srcset.split(",", 1)[0].strip().split(" ", 1)[0]
                if first_src:
                    self.image_urls.append(first_src)

        if tag in {"p", "br", "div", "li", "h1", "h2", "h3", "h4"}:
            self.text_parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1
            return

        if tag in {"p", "div", "li", "h1", "h2", "h3", "h4"}:
            self.text_parts.append("\n")

    def handle_data(self, data):
        if self._skip_depth:
            return

        cleaned = data.strip()
        if cleaned:
            self.text_parts.append(cleaned)

    @property
    def text(self):
        text = " ".join(self.text_parts)
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r" *\n+ *", "\n", text)
        return unescape(text).strip()


def fetch_json(url):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        return response, response.read().decode("utf-8")


def fetch_bytes(url):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        content_type = response.headers.get("content-type", "").split(";")[0]
        return response.read(), content_type


def parse_json_payload(raw_payload):
    import json

    return json.loads(raw_payload)


def strip_html(html):
    parser = ContentParser()
    parser.feed(html or "")
    return parser.text


def truncate(value, max_length):
    value = value or ""
    return value[:max_length]


def absolute_url(url):
    if not url:
        return ""
    return urljoin(SOURCE_URL, unescape(str(url)).strip())


def unique_urls(urls):
    seen = set()
    result = []

    for url in urls:
        absolute = absolute_url(url)
        if not absolute or absolute in seen:
            continue
        if "blank.gif" in absolute or "loading.gif" in absolute:
            continue
        seen.add(absolute)
        result.append(absolute)

    return result


def extract_content(html):
    parser = ContentParser()
    parser.feed(html or "")

    upload_urls = re.findall(
        r"https?://[^\\\"'<> )]+/wp-content/uploads/[^\\\"'<> )]+",
        html or "",
    )

    return parser.text, unique_urls([*parser.image_urls, *upload_urls])


def get_featured_image(post):
    embedded_media = post.get("_embedded", {}).get("wp:featuredmedia", [])
    if not embedded_media:
        return ""

    media = embedded_media[0] or {}
    return (
        media.get("source_url")
        or media.get("media_details", {}).get("sizes", {}).get("large", {}).get("source_url")
        or ""
    )


def get_category_name(post):
    terms_groups = post.get("_embedded", {}).get("wp:term", [])
    for terms in terms_groups:
        for term in terms:
            if term.get("taxonomy") == "category" and term.get("name"):
                return strip_html(term["name"])
    return "News"


def parse_date(value):
    if not value:
        return None, None

    parsed = datetime.fromisoformat(value)
    aware = make_aware(parsed) if parsed.tzinfo is None else parsed
    return aware, aware.date()


def get_filename(url, prefix):
    path = PurePosixPath(urlparse(url).path)
    stem = slugify(path.stem)[:80] or prefix
    suffix = path.suffix.lower()
    if not suffix:
        suffix = mimetypes.guess_extension(mimetypes.guess_type(url)[0] or "") or ".jpg"
    return f"{prefix}-{stem}{suffix}"


class Command(BaseCommand):
    help = "Import all news and media from salymbekov.com WordPress into presscentre."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=None, help="Import only N latest posts.")
        parser.add_argument("--page-size", type=int, default=100, help="WordPress API page size.")
        parser.add_argument("--skip-media", action="store_true", help="Import text only.")
        parser.add_argument("--clear-gallery", action="store_true", help="Replace existing gallery images.")
        parser.add_argument("--dry-run", action="store_true", help="Fetch and parse without saving.")

    def handle(self, *args, **options):
        page_size = min(max(options["page_size"], 1), 100)
        limit = options["limit"]
        dry_run = options["dry_run"]
        skip_media = options["skip_media"]
        clear_gallery = options["clear_gallery"]

        imported = 0
        updated = 0
        created = 0
        page = 1

        while True:
            url = f"{POSTS_URL}?per_page={page_size}&page={page}&_embed=1"
            try:
                response, raw_payload = fetch_json(url)
            except HTTPError as error:
                if error.code == 400 and page > 1:
                    break
                raise CommandError(f"WordPress request failed: {error}") from error
            except URLError as error:
                raise CommandError(f"WordPress request failed: {error}") from error

            posts = parse_json_payload(raw_payload)
            if not posts:
                break

            for post in posts:
                if limit is not None and imported >= limit:
                    self._summary(created, updated, imported, dry_run)
                    return

                was_created = self.import_post(
                    post,
                    dry_run=dry_run,
                    skip_media=skip_media,
                    clear_gallery=clear_gallery,
                )
                imported += 1
                if not dry_run:
                    created += 1 if was_created else 0
                    updated += 0 if was_created else 1

            total_pages = int(response.headers.get("x-wp-totalpages", page))
            if page >= total_pages:
                break
            page += 1

        self._summary(created, updated, imported, dry_run)

    def import_post(self, post, *, dry_run, skip_media, clear_gallery):
        external_id = str(post["id"])
        title = truncate(strip_html(post.get("title", {}).get("rendered", "")) or f"News {external_id}", 255)
        excerpt = strip_html(post.get("excerpt", {}).get("rendered", ""))
        description, content_images = extract_content(post.get("content", {}).get("rendered", ""))
        featured_image = absolute_url(get_featured_image(post))
        source_url = post.get("link", "")
        category_name = truncate(get_category_name(post), 255)
        created_at, published_at = parse_date(post.get("date"))

        if dry_run:
            self.stdout.write(f"[dry-run] {external_id}: {title}")
            return False

        category = self.get_or_create_category(category_name)
        defaults = {
            "category": category,
            "source_url": truncate(source_url, 500),
            "title_en": title,
            "title_ru": title,
            "title_kg": title,
            "short_description_en": excerpt,
            "short_description_ru": excerpt,
            "short_description_kg": excerpt,
            "description_en": description,
            "description_ru": description,
            "description_kg": description,
            "published_at": published_at,
        }

        with transaction.atomic():
            news, created = News.objects.update_or_create(
                external_id=external_id,
                defaults=defaults,
            )

            if created_at:
                News.objects.filter(pk=news.pk).update(created_at=created_at)

            if not skip_media:
                self.save_media(news, featured_image, content_images, clear_gallery=clear_gallery)

        status = "created" if created else "updated"
        self.stdout.write(f"{status}: {external_id} {title}")
        return created

    def get_or_create_category(self, title):
        normalized_title = title or "News"
        category = (
            Category.objects.filter(title_en=normalized_title).first()
            or Category.objects.filter(title_ru=normalized_title).first()
            or Category.objects.filter(title_kg=normalized_title).first()
        )
        if category:
            return category

        return Category.objects.create(
            title_en=normalized_title,
            title_ru=normalized_title,
            title_kg=normalized_title,
        )

    def save_media(self, news, featured_image, content_images, *, clear_gallery):
        if featured_image and not news.image:
            self.download_into_field(news.image, featured_image, f"news-{news.external_id}")
            news.save(update_fields=["image"])

        gallery_urls = [url for url in content_images if url != featured_image]
        if clear_gallery:
            news.gallery.all().delete()
        elif news.gallery.exists():
            return

        for index, image_url in enumerate(gallery_urls):
            gallery_image = NewsImage(news=news, order=index)
            self.download_into_field(gallery_image.image, image_url, f"news-{news.external_id}-{index}")
            gallery_image.save()
            time.sleep(0.05)

    def download_into_field(self, image_field, url, prefix):
        payload, content_type = fetch_bytes(url)
        filename = get_filename(url, prefix)
        if "." not in filename:
            filename += mimetypes.guess_extension(content_type) or ".jpg"
        image_field.save(filename, ContentFile(payload), save=False)

    def _summary(self, created, updated, imported, dry_run):
        style = self.style.WARNING if dry_run else self.style.SUCCESS
        self.stdout.write(style(f"Imported: {imported}. Created: {created}. Updated: {updated}."))
