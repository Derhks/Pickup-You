FROM python:3.9.13

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /code

COPY requirements.txt /code/

RUN pip3 install -r requirements.txt

COPY . /code/
