FROM python:3.11.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/config/requirements.txt
RUN pip install -r requirements.txt

COPY . /code/