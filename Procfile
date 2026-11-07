release: python manage.py verify_media_storage && python manage.py migrate --noinput && python manage.py update_university_2026 --apply --database-backup
web: gunicorn core.wsgi --log-file -
