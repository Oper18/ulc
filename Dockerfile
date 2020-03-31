FROM python:3.7

RUN mkdir /ulc
COPY requirements.txt /ulc/requirements.txt
WORKDIR /ulc
RUN apt-get update -y \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - --error-logfile - ulc.wsgi
