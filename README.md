# gpav
Google+ Archive Viewer

## Prerequisites
* Python 3.7+
  * **If you use macOS, make sure you use the Homebrew version of Python 3**
* Postgres

## Configurations
* `DATABASE_URL` - Mandatory Postgres URL. For development, it should be `postgres://admin:password@localhost:5432/gpav`
* `SECRET_KEY` - Mandatory [Django secret key](https://docs.djangoproject.com/en/3.1/ref/settings/#secret-key)
* `DEBUG` - Optional [Django debug](https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-DEBUG). By default `false`
* `SHOW_PRIVATE_POSTS` - Optional. Whether to show private (non-Public in Google+) posts. By default `false`

## Development
1. Initialize virtualenv and install dependencies
```
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

2. Create the required Postgres database
```
createdb gpav
psql gpav
# create user admin password 'password';
# grant all privileges on database gpav to admin;
```

3. Copy a development environment file
```
cp .example.env .env
```

4. Perform the first migration
```
python manage.py migrate
```

5. Create an admin user for Django admin
```
python manage.py createsuperuser
```
