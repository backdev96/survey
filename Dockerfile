FROM python:3.8.5

RUN mkdir /code
COPY . /code
RUN pip install -r /code/requirements.txt
WORKDIR /code
CMD python3 trood.manage.py migrate && \
    python manage.py loaddata dump.json && \
    python3 trood.manage.py runserver