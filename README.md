# Odoo

## Prerequisite

- [pyenv](https://github.com/pyenv/pyenv)
- [nvm](https://github.com/nvm-sh/nvm)

## Update source

```shell
git submodule init
git submodule update --init --depth 1 --recursive
```

## Build odoo

```shell
sudo apt install postgresql postgresql-client libpq-dev libldap2-dev libsasl2-dev
sudo ./odoo17/setup/debinstall.sh
npm install -g rtlcss
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_amd64.deb -P /tmp
sudo apt install -y /tmp/wkhtmltox_0.12.6.1-3.jammy_amd64.deb
```

## Setup database

```shell
sudo -i -u postgres
psql
```

```sql
CREATE ROLE admin WITH LOGIN PASSWORD 'admin';
\du
CREATE DATABASE odoo OWNER admin;
\l
ALTER ROLE admin WITH SUPERUSER;
ALTER ROLE admin CREATEDB;
\q
```

## Setup odoo

```shell
python -m venv venv
source ./venv/bin/activate
pip install inotify
pip install -r odoo17/requirements.txt
```

## Run odoo

```shell
python odoo17/odoo-bin --dev=all --log-web --log-sql -c odoo.conf
```

## Command

- Create module

```shell
python odoo17/odoo-bin scaffold player addons -t default
```

- Database

```shell
http://localhost:8069/web/database/manager
```

## Note

- Need to create at least 1 database for database/manager to work
