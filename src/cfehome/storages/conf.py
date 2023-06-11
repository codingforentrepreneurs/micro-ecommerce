from cfehome.env import config

AWS_ACCESS_KEY_ID =config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_STORAGE_BUCKET_NAME = 'micro-ecommerce-jd'
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL="public-read"
AWS_S3_VERITY = True


# file upload storage default
DEFAULT_FILE_STORAGE = 'cfehome.storages.backends.MediaStorage'

# staticfiles 
STATICFILES_STORAGE = 'cfehome.storages.backends.StaticFileStorage'