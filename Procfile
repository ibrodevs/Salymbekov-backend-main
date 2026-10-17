release: python manage.py migrate --noinput && python manage.py bootstrap_site_pages && python manage.py fill_empty_cms_from_snapshots && python manage.py seed_home_page
web: gunicorn core.wsgi --log-file -
