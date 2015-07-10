FROM python:3-onbuild
EXPOSE 8000
CMD ["gunicorn", "helper.wsgi:application", "--bind=0:8000"]
