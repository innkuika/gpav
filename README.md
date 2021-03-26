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

## Develepment after setup
1. Enter virtualenv
```
source venv/bin/activate
```

2. Run server
```
python manage.py runserver 
```

## S3 migration for local development
1. Setup S3 bucket
 * Create bucket, don't block public access, use policy:
  ```
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::<bucket name>/*"
        }
    ]
  }
  ```
 
 * Create IAM user and grant permission, enable `Programmatic Access`, use policy:
    ```
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket name>/*",
                "arn:aws:s3:::<bucket name>"
            ]
        }
    ]
    }
   ```
  
2. Fill in env vars in `example.env`
3. Delete all data in database
```
python manage.py delete_all  
```

4. Perform migration
```
python manage.py migrate
```

5. Import data
```
python manage.py import <path/to/archive/directory>
```

## S3 migration for production 
1. Setup s3 bucket (same as step 1 above)
2. Add following config var to heroku:
 * `AWS_STORAGE_BUCKET_NAME`
 * `AWS_SECRET_ACCESS_KEY`
 * `AWS_S3_REGION_NAME`
 * `AWS_ACCESS_KEY_ID`
