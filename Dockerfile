FROM python:3-onbuild
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=helper.settings
RUN SECRET_KEY=foobar PYTHONPATH=. django-admin collectstatic --noinput
CMD ["gunicorn", "helper.wsgi:application", "--bind=0:8000"]
