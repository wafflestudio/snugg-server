# snugg-server
snugg 서버

## PostgreSQL Install
```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql
```

## PostgreSQL Config
```
sudo service postgres restart
sudo -u postgres psql

CREATE DATABASE database;
CREATE USER user WITH PASSWORD 'password';

// https://docs.djangoproject.com/en/4.0/ref/databases/#optimizing-postgresql-s-configuration
ALTER ROLE user SET client_encoding TO 'utf8';
ALTER ROLE user SET default_transaction_isolation TO 'read committed';
ALTER ROLE user SET TIME ZONE 'Asia/Seoul';

GRANT ALL PRIVILEGES ON DATABASE database TO user;
```

## .env Example
```
DJANGO_SECRET_KEY="qwer1234"
DEBUG=True
HOST="54.180.123.137"

POSTGRESQL_NAME="snugg"
POSTGRESQL_USER="snugg"
POSTGRESQL_PASSWORD="qwer1234"
POSTGRESQL_HOST="127.0.0.1"
POSTGRESQL_PORT="5432"
```

## Run Development Server
```
sudo service postgres restart

cd snugg-server

python3 -m venv venv
source venv/bin/activate
sudo apt install libpq-dev python3-dev
pip3 install -r requirements.txt

python3 manage.py migrate
python3 manage.py runserver
```

## Project Apps Directory
```
snugg-server/snugg/apps/
```

## Git hooks
```
pre-commit install
```
