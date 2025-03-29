# Odoo

## Prerequisite

- [pyenv](https://github.com/pyenv/pyenv)
- [nvm](https://github.com/nvm-sh/nvm)

## Clone

```shell
git clone --depth 1 --branch 17.0 git@github.com:odoo/odoo.git odoo17.0
```

## Update source

```shell
git submodule init
git submodule update --init --depth 1 --recursive
```

## Build odoo

```shell
sudo apt install postgresql postgresql-client libpq-dev libldap2-dev libsasl2-dev
sudo ./odoo17.0/setup/debinstall.sh
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
-- Create role with login and password
CREATE ROLE admin WITH LOGIN PASSWORD 'admin';

-- List roles
\du

-- Create database with owner
CREATE DATABASE odoo OWNER admin;
       
-- List databases
\l

-- Grant all privileges to role
ALTER ROLE admin WITH SUPERUSER;
      
-- Grant create database to role
ALTER ROLE admin CREATEDB;
      
-- Quit
\q
```

## Setup odoo

```shell
python -m venv venv
source ./venv/bin/activate
pip install inotify ipdb
pip install -r odoo17.0/requirements.txt
```

## Run odoo

- init odoo

```shell
python odoo17.0/odoo-bin -i base -d odoo -c odoo.conf
```

- run odoo for select database

```shell
python odoo17.0/odoo-bin --dev=all --log-web --log-sql -c odoo.conf
```

## Command

- Create module

```shell
python odoo17.0/odoo-bin scaffold player addons -t default
```

- Select Database

```shell
http://localhost:8069/web/database/manager
```

## Note

- Need to create at least 1 database for database/manager to work

- Debug python

```python
import ipdb; ipdb.set_trace()
```

- Active developer mode & auto reload assets in browser with Chrome Extension [Odoo Debug](https://chromewebstore.google.com/detail/odoo-debug/hmdmhilocobgohohpdpolmibjklfgkbi)
