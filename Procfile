release: python manage.py migrate --noinput && python manage.py bootstrap_site_pages && python manage.py fill_empty_cms_from_snapshots && python manage.py normalize_cms_metadata && python manage.py seed_home_page && python manage.py migrate_external_media --apply
web: gunicorn core.wsgi --log-file -
