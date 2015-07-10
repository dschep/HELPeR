FROM python:3-onbuild
EXPOSE 8000
RUN SECRET_KEY=foobar DJANGO_SETTINGS_MODULE=helper.settings PYTHONPATH=. django-admin collectstatic --noinput
CMD ["gunicorn", "helper.wsgi:application", "--bind=0:8000"]
