# gpav
Google+ Archive Viewer

## Prerequisites
* Python 3.7+
* Postgres

## Configurations
* `SHOW_PRIVATE_POSTS` - whether to show private (non-Public in Google+) posts

## Development
If you are on macOS, make sure you first install Postgres via homebrew

```
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

1. Create the required Postgres database
```
createdb gpav
psql gpav
# create user admin password 'password';
# grant all privileges on database gpav to admin;
```

2. Perform the first migration
```
python manage.py migrate
```

3. Create an admin user for Django admin
```
python manage.py createsuperuser
```

4. Run server
```
python manage.py runserver
```