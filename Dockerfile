FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile* /code/
#RUN pipenv install psycopg2-binary
RUN pipenv install --dev

COPY . /code/