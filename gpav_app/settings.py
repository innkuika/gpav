import os

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
SHOW_PRIVATE_POSTS = os.environ.get('SHOW_PRIVATE_POSTS', 'false') == 'true'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')