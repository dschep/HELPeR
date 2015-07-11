FROM python:3-onbuild
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=helper.settings
# so many vars to avoid key errors in settings file and PYTHONPATH for djadmin
RUN SECRET_KEY=foobar BROKER_URL= DATABASE_URL= PYTHONPATH=. \
    django-admin collectstatic --noinput
CMD ["gunicorn", "helper.wsgi:application", "--bind=0:8000"]
