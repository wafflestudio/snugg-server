FROM python:3.8.9

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt && \
    python3 manage.py migrate

