FROM python:3.9-slim

# Install the necessary packages
RUN apt-get update && \
    apt-get install -y \
      locales apt-utils

# Generate locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

# Set envs that won't change much
ENV LANG="en_US.UTF-8"
ENV LANGUAGE="en_US:en"
ENV LC_ALL="en_US.UTF-8"

# Set application specific envs
ENV DJANGO_SETTINGS_MODULE=trood.settings

# Upgrade pip to the latest version
RUN python -m pip install -U --force-reinstall pip

VOLUME /code/api

EXPOSE 80

ENV NATIONAL_PROJECTS_DB_USER=survey
ENV NATIONAL_PROJECTS_DB_PASSWORD=survey
ENV NATIONAL_PROJECTS_DB_NAME=survey
ENV NATIONAL_PROJECTS_DB_HOST=database
ENV NATIONAL_PROJECTS_DB_PORT=5432

ENV NATIONAL_PROJECTS_STATIC_FILES=/app/static
ENV NATIONAL_PROJECTS_MEDIA_ROOT=/var/www/app/media
VOLUME /var/www/app/media

COPY /api/requirements.txt /code/api/
RUN pip install -r /code/api/requirements.txt

CMD python3 manage.py runserver