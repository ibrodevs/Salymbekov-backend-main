# Сверка контента с salymbekov.com

Страницы нового сайта остаются те же, меняется только их содержимое: тексты, составы, контакты и документы берутся с соответствующих страниц официального сайта salymbekov.com. Все файлы (PDF, фото) переносятся в наш S3-бакет Bucketeer.

## Что входит

- `cms_pages/legacy_parity/payload.json` — содержимое 110 страниц, собранное с salymbekov.com (18.10.2026).
- `tools/build_legacy_parity.py` — скрипт, который собирает этот файл заново (если оригинал обновится).
- `python manage.py apply_legacy_parity` — команда, которая записывает содержимое в CMS.
- Миграция `presscentre/0015`: заголовок новости до 500 символов (один заголовок не помещался в 255).

Новости, главная, баннеры, партнёры, подвал, контакты, «Стартапы», «Научные проекты», «Образовательные услуги» и «Материально-техническая база» не меняются.

## Команды Heroku

Выполнять по порядку, без новых деплоев между шагами 3 и 6. Приложение: `salymbekov-backend`.

1. Резервная копия базы:

   ```bash
   heroku pg:backups:capture -a salymbekov-backend
   ```

2. Влить ветку `fix/legacy-content-parity` в `main` (push в main сам задеплоит сервер). При деплое применится миграция новостей.

3. Посмотреть, что изменится (ничего не записывает):

   ```bash
   heroku run python manage.py apply_legacy_parity -a salymbekov-backend
   ```

4. Записать содержимое:

   ```bash
   heroku run python manage.py apply_legacy_parity --apply -a salymbekov-backend
   ```

5. Перенести файлы с salymbekov.com в S3 (около 700 файлов, 10–30 минут):

   ```bash
   heroku run:detached python manage.py migrate_external_media --apply --strict -a salymbekov-backend
   heroku logs --tail --dyno run -a salymbekov-backend
   ```

   В конце в логе должно быть `Strict CMS media migration passed`.

6. Убрать из галерей и списков документов дубли файлов, которые уже показаны в тексте страницы (сами файлы в S3 остаются):

   ```bash
   heroku run python manage.py apply_legacy_parity --finalize -a salymbekov-backend
   ```

7. Проверка:

   ```bash
   heroku run python manage.py apply_legacy_parity --check -a salymbekov-backend
   ```

   Ожидается `Legacy parity check passed for 110 pages.`

## Откат

```bash
heroku pg:backups -a salymbekov-backend
heroku pg:backups:restore <ID копии из шага 1> DATABASE_URL -a salymbekov-backend --confirm salymbekov-backend
```

## Как обновить данные, если оригинал изменится

```bash
pip install beautifulsoup4
python tools/build_legacy_parity.py --out cms_pages/legacy_parity/payload.json
```

Затем закоммитить файл и повторить шаги 4–7.
