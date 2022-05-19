# Social network

## Description
...

## Run project locally

### 1. Setup environment
You must have **Python 3.10** and **PostgreSQL 14.1/13.5** installed before running the project:

- Python 3.10 - https://www.python.org/downloads/release/python-3100/
- PostgreSQL 14.1/13.5 - https://www.postgresql.org/download/

### 2. Python
```shell
python -m pip install -r requirements.txt
```

### 3. Environment variables
- create `.env` file in the folder where `manage.py` is located
- add environment variables, in particular the database name (_DB_NAME_), username (_DB_USER_), password to log in to
the database (_DB_PASSWORD_), host (_DB_HOST_) and port (_DB_PORT_) on which the database is located. For example:
```shell
DB_USER = postgresql
DB_NAME = social_network
...
```
### 4. PostgreSQL
- sign in **postgresql** from CLI:
```shell
psql postgres <DB_USER>;
```
- create a new database, which we will use in our project:
```shell
CREATE DATABASE <DB_NAME>;
```

### 5. Connect PostgreSQL and Django
- go to the folder with the file ``manage.py``:
```shell
cd path/to/folder
```
- migrate changes to the database:
```shell
python ./manage.py migrate
```

### 6. Run server
```shell
python ./manage.py runserver
```

### 7. Pre-commit
- install **pre-commit**
```shell
pre-commit install
```
```shell
pre-commit --version
```
