"""Build cms_pages/legacy_parity/payload.json from the official WordPress site.

The new site keeps its own sections; this script only makes the content of the
existing CMS pages match their counterparts on https://salymbekov.com.

Usage (from the backend root, any Python 3.10+ with beautifulsoup4):

    python tools/build_legacy_parity.py \
        --reuse-map /path/to/reuse_map.json \
        --out cms_pages/legacy_parity/payload.json

--reuse-map is optional: a JSON object {wordpress_file_url: bucketeer_url}
for files that are byte-identical to files already stored in our S3 bucket,
so they are not downloaded again.
"""

import argparse
import concurrent.futures
import datetime
import html
import json
import re
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup, Comment

WP = "https://salymbekov.com"
UA = {"User-Agent": "Mozilla/5.0 (compatible; SalymbekovParityBuilder/1.0)", "Cookie": "beget=begetok"}
UPLOAD_RE = re.compile(r"^https?://(?:www\.)?salymbekov\.com/wp-content/uploads/", re.I)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".zip", ".rar")
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif")

# ---------------------------------------------------------------------------
# New CMS path -> WordPress page slugs (in display order).
# A page with several sources gets one <h2> section per source.
# ---------------------------------------------------------------------------
PAGES = {
    "/about": ["history-of-university-2"],
    "/founderMessege": ["obrashenie-uchreditelya"],
    "/university/mission": ["mission"],
    "/university/structure/university-main": ["struktura-universiteta"],
    "/university/structure/international-faculty": ["vyshaya-shkola-mediciny"],
    "/university/structure/it-college": ["mezhdunarodnyj-kolledzh-it-i-biznesa"],
    "/university/management/founder": ["uchreditel"],
    "/university/management/rectorate": [
        "rektor",
        "prorektor",
        "prorektor-po-uchebno-vospitatelnoj-rabote",
        "prorektor-po-gosudarstvennomu-yazyku",
        "prorektor-po-klinicheskoj-rabote",
        "pomoshhnik-rektora",
        "prorektor-po-akademicheskoj-rabote",
        "prorektor-po-vospitatelnoj-i-socialnoj-rabote",
        "prorektor-po-administrativno-hozjajstvennoj-rabote",
    ],
    "/university/councils/development-council": ["sovet-razvitija"],
    "/university/councils/academic-council": ["uchenyj-sovet"],
    "/university/councils/educational-council": ["sovet-po-kachestvu"],
    "/university/councils/technical-council": ["uchebno-metodicheskij-sovet"],
    "/university/councils/scientific-council": ["nauchno-tehnicheskij-sovet"],
    "/university/councils/editorial-board": ["redakcionnyj-sovet"],
    "/university/councils/admissions-committee": ["priemnaja-komissija"],
    "/university/councils/commission-support": ["komissija-po-socialnoj-podderzhke-studentov"],
    "/university/councils/bioethics-committee": ["komitet-po-biojetike"],
    "/university/councils/council-scients": ["sovet-volodyh-uchenyh"],
    "/university/councils/employers-council": ["sovet-rabotodatelej"],
    "/university/councils/parents-council": ["sovet-roditelej"],
    "/university/councils/student-councils": ["polozhenie-o-stud-sovete"],
    "/university/normative-docs/kr-acts": ["npa-kr", "normativno-pravovye-akty-kyrgyzskoj-respubliki"],
    "/university/normative-docs/internal-acts": ["npa", "polozhenija-npa", "dolzhnostnye-instrukcii"],
    "/university/normative-docs/licenses": ["licenzii"],
    "/university/normative-docs/logo": ["logotip"],
    "/university/quality-management-system/quality-policy": ["smk", "politika-kachestva", "otchety-smk"],
    "/university/quality-management-system/quality-monitoring": ["monitoring-kachestva"],
    "/education/ait/about": ["ob-institute"],
    "/education/ait/leadership": ["rukovodstvo-instituta"],
    "/education/ait/disciplines": ["discipliny-kolledzha"],
    "/education/ait/teachers": ["prepodavateli-2"],
    "/education/ait/contacts": ["kontakty-2"],
    "/education/mfm/about": ["vyshaya-shkola-mediciny"],
    "/education/mfm/dekanat/dean": ["dekanat"],
    "/education/mfm/dekanat/curriculum": ["uchebnyj-plan-mfm"],
    "/education/mfm/dekanat/departments": [
        "kafedra-egd-2",
        "kafedra-kliniko-morfologicheskih-disciplin",
        "kafedra-kd",
    ],
    "/education/mfm/programs/five-years": ["lechebnoe-delo-5-let"],
    "/education/mfm/programs/six-years": ["lechebnoe-delo-6-let"],
    "/education/it-college/director": ["director-colledja"],
    "/education/it-college/specialties/diplom-computational-sciences": ["kompjuternaja-nauka"],
    "/education/it-college/specialties/diplom-mobile-computing": ["mobilnye-vychislenija"],
    "/education/it-college/specialties/diplom-multimedia-applications": ["multimedijnye-programmy"],
    # The legacy "double diploma" menu item is a 404 on the old site; the
    # programme itself is described on the college page.
    "/education/it-college/double-diploma": ["mezhdunarodnyj-kolledzh-it-i-biznesa"],
    "/education/it-college/departments/general": ["otdelenie-obshheobrazovatelnyh-disciplin"],
    "/education/it-college/departments/information": ["otdelenie-it"],
    "/education/it-college/pedagogical-council": ["pedagogicheskij-sovet-2"],
    "/education/postgrad/internship": ["internatura"],
    "/education/postgrad/residency": ["ordinatura"],
    "/education/postgrad/postgraduate": ["aspirantura"],
    "/education/postgrad/phd": ["phd"],
    "/education/center/about": ["o-centre"],
    "/clinical/doc-clinic": ["doc-university-clinic"],
    "/clinical/doc-hospital": ["doc-university-hospital"],
    "/clinical/simulation-center": ["simuljacionnyj-centr"],
    "/science/management/scientific-technical-council": ["nauchno-tehnicheskij-sovet"],
    "/science/management/bioethics": ["komitet-po-biojetike"],
    "/science/management/young-scientists": ["sovet-volodyh-uchenyh"],
    "/science/management/department": ["departament-nauki-i-perspektivnyh-issledovanij"],
    "/science/labs": ["laboratorii-i-centry"],
    "/science/labs/anatomy": ["anatomicheskij-zal"],
    "/science/labs/biochemistry": ["laboratorija-biohimii"],
    "/science/labs/biology": ["laboratorija-biologii"],
    "/science/labs/computer": ["kompjuternye-klassy"],
    "/science/labs/interactive": ["interaktivnyj-klass"],
    "/science/labs/study": ["uchebnye-klassy"],
    "/science/publications": ["nauchnyj-zhurnal"],
    "/science/publications/journal": [f"vypusk-{i}" for i in range(1, 11)],
    "/science/scholarships": ["stipendii-i-lgoty"],
    "/cooperation/international-partners": ["sotrudnichestvo-s-universitetami"],
    "/cooperation/local-partners": ["sotrudnichestvo_clinics", "jekskljuzivnye-soglashenija"],
    "/vacancies": ["vakansii"],
}

# Titles for pages that aggregate several legacy pages or whose legacy title
# does not describe the new page. Everything else takes the legacy title.
TITLE_OVERRIDES = {
    "/university/management/rectorate": {"ru": "Ректорат", "kg": "Ректорат", "en": "Rectorate"},
    "/university/normative-docs/internal-acts": {
        "ru": "Нормативно-правовые акты университета",
        "kg": "Университеттин ченемдик укуктук актылары",
        "en": "University regulations",
    },
    "/university/normative-docs/kr-acts": {
        "ru": "Нормативно-правовые акты КР",
        "kg": "КРдин ченемдик укуктук актылары",
        "en": "Legal acts of the Kyrgyz Republic",
    },
    "/university/quality-management-system/quality-policy": {
        "ru": "Политика в области качества",
        "kg": "Сапат саясаты",
        "en": "Quality policy",
    },
    "/education/mfm/dekanat/departments": {"ru": "Кафедры", "kg": "Кафедралар", "en": "Departments"},
    "/education/it-college/double-diploma": {
        "ru": "Программа двойного диплома",
        "kg": "Кош диплом программасы",
        "en": "Double degree programme",
    },
    "/science/publications/journal": {
        "ru": "Научный журнал «Вестник медицины и образования»",
        "kg": "«Медицина жана билим берүү жарчысы» илимий журналы",
        "en": "Scientific journal “Bulletin of Medicine and Education”",
    },
}

# Navigation-only pages: no legacy text exists, so the page lists its subpages.
NAV_PAGES = {
    "/university/structure": {
        "title": {"ru": "Структура университета", "kg": "Университеттин түзүмү", "en": "University structure"},
        "links": ["/university/structure/university-main", "/university/structure/international-faculty", "/university/structure/it-college"],
    },
    "/university/management": {
        "title": {"ru": "Органы управления", "kg": "Башкаруу органдары", "en": "Governing bodies"},
        "links": ["/university/management/founder", "/university/management/rectorate", "/university/management/public-councils"],
    },
    "/university/management/public-councils": {
        "title": {"ru": "Общественные советы", "kg": "Коомдук кеңештер", "en": "Public councils"},
        "links": [
            "/university/councils/development-council", "/university/councils/academic-council",
            "/university/councils/educational-council", "/university/councils/technical-council",
            "/university/councils/scientific-council", "/university/councils/editorial-board",
            "/university/councils/admissions-committee", "/university/councils/commission-support",
            "/university/councils/bioethics-committee", "/university/councils/council-scients",
            "/university/councils/employers-council", "/university/councils/parents-council",
            "/university/councils/student-councils",
        ],
    },
    "/university/normative-docs": {
        "title": {"ru": "Нормативные документы", "kg": "Ченемдик документтер", "en": "Regulatory documents"},
        "links": ["/university/normative-docs/kr-acts", "/university/normative-docs/internal-acts", "/university/normative-docs/licenses", "/university/normative-docs/logo"],
    },
    "/education/ait": {
        "title": {"ru": "Американский институт технологий", "kg": "Америка технологиялар институту", "en": "American Institute of Technology"},
        "links": ["/education/ait/about", "/education/ait/leadership", "/education/ait/disciplines", "/education/ait/teachers", "/education/ait/contacts"],
    },
    "/education/mfm": {
        "title": {"ru": "Высшая школа медицины", "kg": "Жогорку медицина мектеби", "en": "Higher School of Medicine"},
        "links": ["/education/mfm/about", "/education/mfm/dekanat/dean", "/education/mfm/dekanat/curriculum", "/education/mfm/dekanat/departments", "/education/mfm/programs/five-years", "/education/mfm/programs/six-years"],
    },
    "/education/it-college": {
        "title": {"ru": "Международный колледж IT и бизнеса", "kg": "IT жана бизнес эл аралык колледжи", "en": "International College of IT and Business"},
        "links": ["/university/structure/it-college", "/education/it-college/director", "/education/it-college/specialties/diplom-computational-sciences", "/education/it-college/specialties/diplom-multimedia-applications", "/education/it-college/specialties/diplom-mobile-computing", "/education/it-college/double-diploma", "/education/it-college/departments/general", "/education/it-college/departments/information", "/education/it-college/pedagogical-council"],
    },
    "/education/postgrad": {
        "title": {"ru": "Факультет последипломного образования", "kg": "Дипломдон кийинки билим берүү факультети", "en": "Faculty of Postgraduate Education"},
        "links": ["/education/postgrad/internship", "/education/postgrad/residency", "/education/postgrad/postgraduate", "/education/postgrad/phd"],
    },
    "/education/center": {
        "title": {"ru": "Центр образования и инноваций в г. Нарын", "kg": "Нарын шаарындагы билим берүү жана инновациялар борбору", "en": "Education and Innovation Centre in Naryn"},
        "links": ["/education/center/about"],
    },
    "/science/management": {
        "title": {"ru": "Органы управления наукой", "kg": "Илимди башкаруу органдары", "en": "Science governance"},
        "links": ["/science/management/scientific-technical-council", "/science/management/bioethics", "/science/management/young-scientists", "/science/management/department"],
    },
    "/science/management/scientific-council": {
        "title": {"ru": "Научно-технический совет", "kg": "Илимий-техникалык кеңеш", "en": "Scientific and Technical Council"},
        "links": ["/science/management/scientific-technical-council"],
    },
    "/science/department": {
        "title": {"ru": "Отдел науки и повышения квалификации", "kg": "Илим жана квалификацияны жогорулатуу бөлүмү", "en": "Department of Science and Professional Development"},
        "links": ["/science/management/department"],
    },
    "/science/events": {
        "title": {"ru": "Научные мероприятия", "kg": "Илимий иш-чаралар", "en": "Scientific events"},
        "links": ["/science/events/conferences"],
    },
    "/infrastructure/locations": {
        "title": {"ru": "Материально-техническая база", "kg": "Материалдык-техникалык база", "en": "Facilities"},
        "links": ["/MaterialBaseGallery", "/science/labs"],
    },
    "/infrastructure/partners": {
        "title": {"ru": "Партнёры", "kg": "Өнөктөштөр", "en": "Partners"},
        "links": ["/cooperation/international-partners", "/cooperation/local-partners"],
    },
}

# /science/events/conferences/<n> -> WordPress post id (all of them are news posts).
CONFERENCES = {
    1: 18045, 2: 18035, 3: 17300, 4: 16024, 5: 15997, 6: 15958, 7: 15839, 8: 15321,
    9: 14372, 10: 14435, 11: 14449, 12: 14507, 13: 14397, 14: 14524, 15: 14950,
    16: 14460, 17: 14292, 18: 14250, 19: 12041, 20: 11955, 21: 11881, 22: 11856, 23: 11017,
}

# Legacy page slug -> new path, used to rewrite internal links.
LEGACY_LINKS = {
    "history-of-university-2": "/about",
    "obrashenie-uchreditelya": "/founderMessege",
    "mission": "/university/mission",
    "struktura-universiteta": "/university/structure/university-main",
    "vyshaya-shkola-mediciny": "/education/mfm/about",
    "mezhdunarodnyj-kolledzh-it-i-biznesa": "/university/structure/it-college",
    "uchreditel": "/university/management/founder",
    "rektor": "/university/management/rectorate",
    "rektorat": "/university/management/rectorate",
    "contact": "/contacts",
    "vakansii": "/vacancies",
    "doc-university-clinic": "/clinical/doc-clinic",
    "doc-university-hospital": "/clinical/doc-hospital",
    "simuljacionnyj-centr": "/clinical/simulation-center",
    "nauchnyj-zhurnal": "/science/publications",
    "stipendii-i-lgoty": "/science/scholarships",
    "sotrudnichestvo-s-universitetami": "/cooperation/international-partners",
    "sotrudnichestvo_clinics": "/cooperation/local-partners",
    "politika-kachestva": "/university/quality-management-system/quality-policy",
    "monitoring-kachestva": "/university/quality-management-system/quality-monitoring",
    "komitet-po-biojetike": "/science/management/bioethics",
    "nauchno-tehnicheskij-sovet": "/science/management/scientific-technical-council",
    "sovet-volodyh-uchenyh": "/science/management/young-scientists",
    "departament-nauki-i-perspektivnyh-issledovanij": "/science/management/department",
    "priemnaja-komissija": "/university/councils/admissions-committee",
    "ob-institute": "/education/ait/about",
    "dekanat": "/education/mfm/dekanat/dean",
    "lechebnoe-delo-5-let": "/education/mfm/programs/five-years",
    "lechebnoe-delo-6-let": "/education/mfm/programs/six-years",
    "internatura": "/education/postgrad/internship",
    "ordinatura": "/education/postgrad/residency",
    "aspirantura": "/education/postgrad/postgraduate",
    "phd": "/education/postgrad/phd",
    "o-centre": "/education/center/about",
    "licenzii": "/university/normative-docs/licenses",
    "logotip": "/university/normative-docs/logo",
}
LEGACY_LINKS.update({f"vypusk-{i}": "/science/publications/journal" for i in range(1, 11)})

# English news: misspellings of the university name produced by translation.
NEWS_EN_REPLACEMENTS = {"Salykbekov": "Salymbekov", "Salybekov": "Salymbekov", "Salymsbekov": "Salymbekov"}

KEEP_ATTRS = {"a": {"href"}, "img": {"src", "alt"}, "td": {"colspan", "rowspan"}, "th": {"colspan", "rowspan"}}
DROP_TAGS = {"style", "script", "noscript", "iframe", "form", "input", "button", "select", "textarea", "svg", "link", "meta"}


def fetch_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        return json.load(r), r.headers


def fetch_all(kind, lang, fields):
    base = f"{WP}/{lang}/wp-json/wp/v2/{kind}?per_page=100&_fields={fields}"
    first, headers = fetch_json(base + "&page=1")
    out = list(first)
    for page in range(2, int(headers.get("X-WP-TotalPages", 1)) + 1):
        out += fetch_json(f"{base}&page={page}")[0]
    return out


def strip_size(url):
    return re.sub(r"-\d+x\d+(?=\.\w+$)", "", url)


def is_upload(url):
    return bool(url) and bool(UPLOAD_RE.match(url))


class Cleaner:
    def __init__(self, reuse_map):
        self.reuse = reuse_map
        self.assets = set()

    def file_url(self, url):
        url = html.unescape(url.strip())
        return self.reuse.get(url, url)

    def clean(self, raw):
        raw = re.sub(r"\[/?[a-zA-Z0-9_-]+(?:\s[^\]]*)?\]", "", raw)  # shortcodes
        soup = BeautifulSoup(raw, "html.parser")
        for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
            c.extract()
        # <a href="file.pdf"><button>PDF</button></a>: keep the button text
        for b in soup.find_all("button"):
            b.unwrap()
        for t in soup.find_all(DROP_TAGS):
            video = re.search(r"youtube\.com/embed/([\w-]+)", t.get("src") or "") if t.name == "iframe" else None
            if video:
                a = soup.new_tag("a", href=f"https://www.youtube.com/watch?v={video.group(1)}")
                a.string = "Видео на YouTube"
                p = soup.new_tag("p")
                p.append(a)
                t.replace_with(p)
            else:
                t.decompose()
        # Robo Gallery keeps image URLs in data attributes instead of <img>
        for block in soup.select(".rbs-img"):
            source = block.select_one("[data-popup]") or block.select_one("[data-thumbnail]")
            url = source and (source.get("data-popup") or source.get("data-thumbnail"))
            if url:
                block.replace_with(soup.new_tag("img", src=url, alt=source.get("title", "")))
            else:
                block.decompose()
        # slider thumbnails duplicate the slides
        for t in soup.select(".sp-thumbnail, .sp-thumbnails"):
            t.decompose()
        # accordion headers: <h3 class="ea-header"><a href="#">Title</a></h3>
        for a in soup.select(".ea-header a"):
            for i in a.find_all("i"):
                i.decompose()
            a.unwrap()
        # images
        seen_imgs = set()
        for img in soup.find_all("img"):
            src = img.get("data-layzr") or img.get("data-lazy-src") or img.get("data-src") or img.get("src") or ""
            if src.startswith("data:") or not src:
                img.decompose()
                continue
            src = html.unescape(src)
            key = strip_size(src)
            if key in seen_imgs:
                img.decompose()
                continue
            seen_imgs.add(key)
            img.attrs = {"src": src, "alt": img.get("alt", "")}
        # links
        for a in soup.find_all("a"):
            href = html.unescape((a.get("href") or "").strip())
            if not href or href.startswith("#") or href.startswith("javascript"):
                a.unwrap()
                continue
            low = urllib.parse.urlparse(href).path.lower()
            if is_upload(href) and low.endswith(IMG_EXT):
                a.unwrap()  # lightbox link around an image
                continue
            if is_upload(href) or "bucketeer" in href:
                a.attrs = {"href": self.file_url(href)}
                label = a.get_text(" ", strip=True)
                # PDF-embedder links show the bare file name; give them a readable label
                if not label or re.fullmatch(r"[a-z0-9._\-]+", label):
                    a.clear()
                    a.append("Открыть документ")
                continue
            m = re.match(r"^https?://(?:www\.)?salymbekov\.com/(?:ru/|kg/|en/)?([^/?#]+)/?$", href)
            if m:
                target = LEGACY_LINKS.get(m.group(1))
                if target:
                    a.attrs = {"href": target}
                else:
                    a.unwrap()
                continue
            if re.match(r"^https?://(?:www\.)?salymbekov\.com/?$", href):
                a.attrs = {"href": "/"}
                continue
            if href == "http://1":
                a.unwrap()
                continue
            a.attrs = {"href": href}
        # attributes
        for t in soup.find_all(True):
            if t.name in ("a", "img"):
                continue
            keep = KEEP_ATTRS.get(t.name, set())
            t.attrs = {k: v for k, v in t.attrs.items() if k in keep}
        # layout wrappers
        for t in soup.find_all(["div", "span", "section", "article", "figure", "font", "center", "i"]):
            if t.name == "figure":
                t.name = "p"
            elif t.name in ("div", "section", "article"):
                t.unwrap()
            elif t.name in ("span", "font", "center"):
                t.unwrap()
        for t in soup.find_all("figcaption"):
            t.name = "p"
        # WordPress wraps accordions and tables in <p>; block content cannot live inside <p>
        for t in soup.find_all("p"):
            if t.find(["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "table", "hr"]):
                t.unwrap()
        html_out = str(soup)
        html_out = html_out.replace("\xa0", " ")
        html_out = re.sub(r"<p>\s*(?:&nbsp;|<br/?>|\s)*</p>", "", html_out)
        html_out = re.sub(r"<(strong|b|em)>\s*</\1>", "", html_out)
        html_out = re.sub(r"\n{3,}", "\n\n", html_out).strip()
        # collect assets
        soup2 = BeautifulSoup(html_out, "html.parser")
        for img in soup2.find_all("img"):
            if is_upload(img["src"]):
                self.assets.add(img["src"])
        for a in soup2.find_all("a"):
            if is_upload(a.get("href", "")):
                self.assets.add(a["href"])
        return html_out


def check_url(url):
    req = urllib.request.Request(url, headers={**UA, "Range": "bytes=0-0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            final = r.geturl()
            return url, r.status in (200, 206) and is_upload(final)
    except Exception:
        return url, False


def drop_broken(body, broken):
    if not broken:
        return body
    soup = BeautifulSoup(body, "html.parser")
    for img in soup.find_all("img"):
        if img.get("src") in broken:
            img.decompose()
    for a in soup.find_all("a"):
        if a.get("href") in broken:
            a.unwrap()
    return str(soup)


def links_html(paths, titles):
    items = "".join(f'<li><a href="{p}">{html.escape(titles.get(p, p))}</a></li>' for p in paths)
    return f"<ul>{items}</ul>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reuse-map")
    ap.add_argument("--out", default="cms_pages/legacy_parity/payload.json")
    ap.add_argument("--new-api", default="https://salymbekov-backend-f4c797e9b169.herokuapp.com/api")
    args = ap.parse_args()

    reuse = json.load(open(args.reuse_map, encoding="utf-8")) if args.reuse_map else {}
    cleaner = Cleaner(reuse)

    print("Fetching WordPress pages/posts…", file=sys.stderr)
    pages = {lang: {x["slug"]: x for x in fetch_all("pages", lang, "id,slug,link,title,content,modified")} for lang in ("ru", "kg", "en")}
    posts = {x["id"]: x for x in fetch_all("posts", "ru", "id,slug,link,title,content,date")}

    # current titles of new pages (for nav lists)
    new_titles = {}
    url = f"{args.new_api}/pages/?lang=ru"
    while url:
        data, _ = fetch_json(url)
        for x in data["results"]:
            new_titles[x["path"]] = x["title"]
        url = data.get("next")

    out_pages = []

    def legacy_title(slug, lang):
        return html.unescape(pages[lang][slug]["title"]["rendered"]).strip()

    for path, slugs in PAGES.items():
        missing = [s for s in slugs if s not in pages["ru"]]
        if missing:
            raise SystemExit(f"{path}: missing legacy pages {missing}")
        titles = TITLE_OVERRIDES.get(path) or {lang: legacy_title(slugs[0], lang) for lang in ("ru", "kg", "en")}
        parts = []
        for slug in slugs:
            body = cleaner.clean(pages["ru"][slug]["content"]["rendered"])
            if not BeautifulSoup(body, "html.parser").get_text(strip=True) and "<img" not in body and "<a" not in body:
                continue
            if len(slugs) > 1:
                parts.append(f"<h2>{html.escape(legacy_title(slug, 'ru'))}</h2>")
            parts.append(body)
        out_pages.append({
            "path": path,
            "title": titles,
            "body_ru": "\n".join(parts),
            "sources": [pages["ru"][s]["link"].replace("/en/", "/ru/") for s in slugs],
            "source_modified": max(pages["ru"][s]["modified"] for s in slugs),
        })
        new_titles[path] = titles["ru"]

    conf_items = []
    for n, post_id in sorted(CONFERENCES.items()):
        post = posts[post_id]
        title = html.unescape(post["title"]["rendered"]).strip()
        date = datetime.date.fromisoformat(post["date"][:10])
        body = f"<p><strong>Дата публикации: {date:%d.%m.%Y}</strong></p>\n" + cleaner.clean(post["content"]["rendered"])
        path = f"/science/events/conferences/{n}"
        out_pages.append({
            "path": path,
            "title": {"ru": title, "kg": title, "en": title},
            "body_ru": body,
            "sources": [post["link"].replace("/en/", "/ru/")],
            "source_modified": post["date"],
        })
        conf_items.append((date, path, title))
    conf_list = "".join(
        f'<li><a href="{p}">{html.escape(t)}</a> — {d:%d.%m.%Y}</li>' for d, p, t in sorted(conf_items, reverse=True)
    )
    out_pages.append({
        "path": "/science/events/conferences",
        "title": {"ru": "Научные конференции", "kg": "Илимий конференциялар", "en": "Scientific conferences"},
        "body_ru": f"<ul>{conf_list}</ul>",
        "sources": [f"{WP}/ru/nauchnye-konferencii/"],
        "source_modified": max(d for d, _, _ in conf_items).isoformat(),
    })

    for path, spec in NAV_PAGES.items():
        out_pages.append({
            "path": path,
            "title": spec["title"],
            "body_ru": links_html(spec["links"], new_titles),
            "sources": [],
            "source_modified": None,
        })

    print(f"Checking {len(cleaner.assets)} legacy files…", file=sys.stderr)
    with concurrent.futures.ThreadPoolExecutor(16) as pool:
        results = dict(pool.map(check_url, sorted(cleaner.assets)))
    broken = {u for u, ok in results.items() if not ok}
    for page in out_pages:
        page["body_ru"] = drop_broken(page["body_ru"], broken)

    payload = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "source": WP,
        "pages": out_pages,
        "news_title_fixes": {"17380": html.unescape(posts[17380]["title"]["rendered"]).strip()} if 17380 in posts else {},
        "news_en_replacements": NEWS_EN_REPLACEMENTS,
        "broken_legacy_files_skipped": sorted(broken),
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    print(
        f"pages={len(out_pages)} legacy_files={len(cleaner.assets) - len(broken)} broken_skipped={len(broken)} "
        f"reused_from_s3={sum(1 for p in out_pages for u in reuse.values() if u in p['body_ru'])}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
