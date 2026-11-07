"""Reviewable, idempotent November 2026 CMS update. Historical news are excluded."""
import re
from django.apps import apps
from django.db import models
from bs4 import BeautifulSoup
from django_ckeditor_5.fields import CKEditor5Field

RENAMES = [
    (r'Центр образования и инноваци[йи] (?:в (?:г\.? )?Нарыне?|\(г\. Нарын\))', 'Нарын кампус'),
    (r'Центр Нарына', 'Нарын кампус'),
    (r'Education and Innovation Cent(?:er|re)(?: in Naryn| \(Naryn\))', 'Naryn Campus'),
    (r'Нарын шаарындагы билим берүү жана инноваци(?:я|ялар) борбору', 'Нарын кампусу'),
    (r'Билим жана инновация борбору \(Нарын шаары\)', 'Нарын кампусу'),
    (r'Высш(?:ая|ей|ую) школ(?:а|ы|у) медицины', 'ИГН'),
    (r'Higher School of Medicine', 'ИГН'),
    (r'Жогорку медицина мектеби', 'ИГН'),
]


def is_retired(url):
    from urllib.parse import urlsplit
    path = urlsplit(str(url or '')).path.rstrip('/')
    return path == '/education/postgrad' or path.startswith('/education/postgrad/')


RETIRED_TITLES = {
    'последипломное образование', 'факультет последипломного образования',
    'postgraduate education', 'faculty of postgraduate education',
    'дипломдон кийинки билим берүү',
}


def retired_title(value):
    return str(value or '').strip().casefold() in RETIRED_TITLES


def retired_navigation_item(item):
    if not isinstance(item, dict):
        return False
    return (
        any(is_retired(item.get(key)) for key in ('url', 'href', 'path', 'link'))
        or any(retired_title(item.get(key)) for key in ('title', 'title_ru', 'title_en', 'title_kg'))
    )


def rewrite(value):
    if isinstance(value, list):
        return [rewrite(item) for item in value if not retired_navigation_item(item)]
    if isinstance(value, dict):
        return {k: rewrite(v) for k, v in value.items()}
    if not isinstance(value, str):
        return value
    # Do not rename another institution's department.
    if not re.search(r'Nazarbayev|Назарбаев', value, re.I):
        for pattern, replacement in RENAMES:
            value = re.sub(pattern, replacement, value, flags=re.I)
    if '<a' in value and '/education/postgrad' in value:
        soup = BeautifulSoup(value, 'html.parser')
        for anchor in soup.find_all('a', href=True):
            if is_retired(anchor['href']):
                # Remove its whole linked card if the title is inside the anchor.
                anchor.decompose()
        value = str(soup)
    return '/education' if is_retired(value) else value


def content_models():
    # News/publications, original documents and historical reports remain intact.
    labels = ['cms_pages', 'about', 'contact_pages']
    return [m for m in apps.get_models() if m._meta.app_label in labels and not m._meta.proxy
            and m.__name__ not in ['DevelopmentCouncilMember', 'ScientificTechnicalCouncilMember', 'ContentSnapshot']]


def apply_update():
    counts = {}
    for model in content_models():
        count = 0
        queryset = model.objects.all()
        if any(field.name == 'page' for field in model._meta.fields):
            queryset = queryset.select_related('page')
        for obj in queryset.iterator():
            if is_retired(getattr(getattr(obj, 'page', None), 'path', '')):
                continue  # Keep archived descendants intact, including their original rich text.
            path = getattr(obj, 'path', '')
            changes = []
            if is_retired(path):
                # Archive entire subtree without rewriting its original content.
                flag = 'is_published' if hasattr(obj, 'is_published') else 'is_active'
                if getattr(obj, flag, False):
                    setattr(obj, flag, False); changes.append(flag)
            else:
                if model.__name__ in ('PageCard', 'PageSection') and obj.is_active and any(retired_title(getattr(obj, 'title_'+lang, '')) for lang in ('ru','en','kg')):
                    obj.is_active = False; changes.append('is_active')
                retired_link = model.__name__ in ('FooterLink', 'PageLink') and is_retired(getattr(obj, 'url', ''))
                if retired_link:
                    obj.is_active = False; changes.append('is_active')
                for field in model._meta.concrete_fields:
                    if field.name in ['path', 'slug', 'internal_notes', 'external_url'] or isinstance(field, models.FileField):
                        continue
                    if not isinstance(field, (models.CharField, models.TextField, models.JSONField, CKEditor5Field)):
                        continue
                    old = getattr(obj, field.name)
                    new = rewrite(old)
                    if new != old:
                        setattr(obj, field.name, new); changes.append(field.name)
            if path == '/education/center/about':
                # Old snapshots used generic or Russian titles even in other languages.
                titles = {'ru': 'О кампусе', 'en': 'About the campus', 'kg': 'Кампус жөнүндө'}
                generic = {'', 'о центре', 'about', 'about center', 'about the center', 'борбор жөнүндө'}
                for lang, title in titles.items():
                    for base in ('title', 'seo_title'):
                        field = f'{base}_{lang}'
                        if hasattr(obj, field) and getattr(obj, field).strip().casefold() in generic:
                            setattr(obj, field, title)
                            changes.append(field)
                if hasattr(obj, 'admin_title') and obj.admin_title.strip().casefold() in generic:
                    obj.admin_title = titles['ru']; changes.append('admin_title')
            if changes:
                obj.save(update_fields=changes); count += 1
        counts[model._meta.label] = count
    from cms_pages.models import Page, PageSection
    for slug, titles, blocks in NEW_PAGES:
        page, created = Page.objects.get_or_create(path='/education'+slug, defaults={
            'admin_title': titles[0], 'navigation_group': 'education', 'force_backend_render': True,
            'data': {'render_mode': 'structured', 'sections_layout': 'grid'},
            **{f'subtitle_{lang}': INTRO[slug][i] for i, lang in enumerate(('ru','en','kg'))},
            **{f'title_{lang}': titles[i] for i, lang in enumerate(('ru','en','kg'))},
            **{f'seo_title_{lang}': titles[i]+' | Salymbekov University' for i, lang in enumerate(('ru','en','kg'))},
            **{f'seo_description_{lang}': titles[i]+' — Salymbekov University' for i, lang in enumerate(('ru','en','kg'))},
            'internal_notes': 'Тексты, сроки, документы и контакты требуют утверждения заказчиком. Цены и сроки не выдумывать.',
        })
        if created:
            for order, (labels, url) in enumerate(blocks):
                PageSection.objects.create(page=page, order=order,
                    **{f'title_{lang}': labels[i] for i, lang in enumerate(('ru','en','kg'))},
                    **{f'body_{lang}': f'<p>{DESCRIPTIONS[slug][i][order]}</p><p><a href="{url}">{LINK_COPY[i]} →</a></p>' for i, lang in enumerate(('ru','en','kg'))})
        counts[page.path] = int(created)
    return counts


LINK_COPY = ('Актуальная информация и контакты', 'Current information and contacts', 'Актуалдуу маалымат жана байланыштар')
NEW_PAGES = [
 ('', ('Программы','Programs','Программалар'), [
   (('Академия инновационных технологий','Academy of Innovative Technologies','Инновациялык технологиялар академиясы'),'/education/ait'),
   (('Международный факультет медицины','International Faculty of Medicine','Эл аралык медицина факультети'),'/education/mfm'),
   (('IT колледж','IT College','IT колледж'),'/education/it-college'),
   (('Нарын кампус','Naryn Campus','Нарын кампусу'),'/education/center'),
   (('Студенту','For students','Студенттерге'),'/education/student'),
   (('Абитуриенту','For applicants','Абитуриенттерге'),'/education/applicant')]),
 ('/student', ('Студенту','For students','Студенттерге'), [
   (('Общая информация','General information','Жалпы маалымат'),'/about'),
   (('Учебный процесс и расписание','Studies and timetable','Окуу процесси жана жадыбал'),'/contact'),
   (('Академический календарь','Academic calendar','Академиялык календарь'),'/contact'),
   (('Учебные ресурсы и библиотека','Learning resources and library','Окуу ресурстары жана китепкана'),'/services'),
   (('Студенческие сервисы','Student services','Студенттик кызматтар'),'/services'),
   (('Поддержка студентов','Student support','Студенттерди колдоо'),'/contact'),
   (('Часто задаваемые вопросы','Frequently asked questions','Көп берилүүчү суроолор'),'/contact'),
   (('Контакты подразделений','Department contacts','Бөлүмдөрдүн байланыштары'),'/contact')]),
 ('/applicant', ('Абитуриенту','For applicants','Абитуриенттерге'), [
   (('Информация о поступлении','Admission information','Кабыл алуу жөнүндө маалымат'),'/university/councils/admissions-committee'),
   (('Образовательные программы','Educational programs','Билим берүү программалары'),'/education'),
   (('Правила и этапы поступления','Admission rules and stages','Кабыл алуу эрежелери жана этаптары'),'/university/councils/admissions-committee'),
   (('Необходимые документы','Required documents','Керектүү документтер'),'/university/councils/admissions-committee'),
   (('Сроки приёма документов','Application deadlines','Документтерди кабыл алуу мөөнөттөрү'),'/university/councils/admissions-committee'),
   (('Стоимость обучения и льготы','Tuition and financial support','Окуу акысы жана жеңилдиктер'),'/university/councils/admissions-committee'),
   (('Часто задаваемые вопросы','Frequently asked questions','Көп берилүүчү суроолор'),'/university/councils/admissions-committee'),
   (('Контакты приёмной комиссии','Admissions committee contacts','Кабыл алуу комиссиясынын байланыштары'),'/university/councils/admissions-committee')]),
]


INTRO = {
 '': ('Образовательные подразделения и полезная информация для студентов и поступающих.', 'Academic departments and useful information for students and applicants.', 'Билим берүү бөлүмдөрү жана студенттер менен абитуриенттер үчүн пайдалуу маалымат.'),
 '/student': ('Всё необходимое для учёбы и университетской жизни: ресурсы, сервисы и поддержка.', 'Resources, services and support for your studies and university life.', 'Окуу жана университеттик жашоо үчүн ресурстар, кызматтар жана колдоо.'),
 '/applicant': ('Найдите программу и узнайте, где уточнить условия поступления в Salymbekov University.', 'Explore programs and find out where to confirm admission requirements at Salymbekov University.', 'Salymbekov University программалары жана кабыл алуу шарттарын тактоо үчүн пайдалуу маалымат.'),
}
DESCRIPTIONS = {
 '': [
  ['О подразделении, учебных направлениях и контактах.', 'Программы и информация о медицинском образовании.', 'Направления подготовки и информация о колледже.', 'Образование и возможности кампуса в Нарыне.', 'Учебные ресурсы, сервисы и поддержка студентов.', 'Программы и информация для поступающих.'],
  ['About the academy, study areas and contacts.', 'Programs and information about medical education.', 'Study areas and college information.', 'Education and opportunities at the Naryn campus.', 'Learning resources, services and student support.', 'Programs and information for applicants.'],
  ['Академия, окуу багыттары жана байланыштар.', 'Медициналык билим берүү программалары.', 'Окуу багыттары жана колледж жөнүндө маалымат.', 'Нарын кампусундагы билим берүү мүмкүнчүлүктөрү.', 'Окуу ресурстары, кызматтар жана студенттерди колдоо.', 'Программалар жана абитуриенттер үчүн маалымат.']],
 '/student': [
  ['Познакомьтесь с университетом и его образовательной средой.', 'Уточните действующее расписание в ответственном подразделении.', 'Запросите актуальный календарь учебного года.', 'Информация об учебных ресурсах и доступных услугах.', 'Узнайте о доступных университетских сервисах.', 'Обратитесь в университет за помощью по учебным вопросам.', 'Не нашли ответ? Направьте свой вопрос в университет.', 'Найдите контакты университета для связи с нужным подразделением.'],
  ['Learn about the university and its learning environment.', 'Confirm your current timetable with the responsible department.', 'Request the current academic calendar.', 'Information about learning resources and available services.', 'Explore university services.', 'Contact the university for help with study-related questions.', 'Need an answer? Send your question to the university.', 'Find university contacts to reach the relevant department.'],
  ['Университет жана анын билим берүү чөйрөсү менен таанышыңыз.', 'Учурдагы жадыбалды жооптуу бөлүмдөн тактаңыз.', 'Учурдагы окуу жылынын календарын сураңыз.', 'Окуу ресурстары жана жеткиликтүү кызматтар жөнүндө маалымат.', 'Университеттин кызматтары жөнүндө билиңиз.', 'Окуу боюнча жардам алуу үчүн университетке кайрылыңыз.', 'Жооп табылган жокпу? Университетке суроо жөнөтүңүз.', 'Керектүү бөлүм менен байланышуу үчүн университеттин байланыштарын табыңыз.']],
 '/applicant': [
  ['Основную информацию и консультацию предоставляет приёмная комиссия.', 'Познакомьтесь с образовательными подразделениями университета.', 'Действующие правила и этапы уточните в приёмной комиссии.', 'Запросите актуальный перечень документов для выбранной программы.', 'Подтвердите сроки подачи документов в приёмной комиссии.', 'Официальную стоимость и условия льгот уточните перед подачей документов.', 'Вопросы о поступлении можно направить приёмной комиссии.', 'Перейдите к информации о приёмной комиссии.'],
  ['Contact the admissions committee for information and guidance.', 'Explore the university’s academic departments.', 'Confirm the current admission rules and stages with the committee.', 'Request the current document checklist for your chosen program.', 'Confirm application deadlines with the admissions committee.', 'Confirm official tuition fees and financial support conditions before applying.', 'Send admission questions to the admissions committee.', 'View information about the admissions committee.'],
  ['Маалымат жана кеңеш алуу үчүн кабыл алуу комиссиясына кайрылыңыз.', 'Университеттин билим берүү бөлүмдөрү менен таанышыңыз.', 'Кабыл алуунун учурдагы эрежелерин жана этаптарын комиссиядан тактаңыз.', 'Тандалган программа үчүн керектүү документтердин тизмесин сураңыз.', 'Документтерди тапшыруу мөөнөттөрүн кабыл алуу комиссиясынан тактаңыз.', 'Документ тапшырардан мурун расмий окуу акысын жана жеңилдик шарттарын тактаңыз.', 'Кабыл алуу боюнча суроолорду комиссияга жөнөтүңүз.', 'Кабыл алуу комиссиясы жөнүндө маалыматка өтүңүз.']],
}
