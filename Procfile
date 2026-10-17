release: python manage.py migrate --noinput && python manage.py bootstrap_site_pages
web: gunicorn core.wsgi --log-file -
