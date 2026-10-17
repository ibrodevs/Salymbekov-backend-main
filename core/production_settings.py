"""Production-only Django settings.

Heroku's filesystem is ephemeral, so every uploaded media file must be stored in
Bucketeer/S3.  This module intentionally fails fast if the Bucketeer config is
missing instead of silently falling back to local /media storage.
"""

import os

from django.core.exceptions import ImproperlyConfigured

from .settings import *  # noqa: F401,F403


BUCKETEER_REQUIRED_VARS = (
    "BUCKETEER_AWS_ACCESS_KEY_ID",
    "BUCKETEER_AWS_SECRET_ACCESS_KEY",
    "BUCKETEER_AWS_REGION",
    "BUCKETEER_BUCKET_NAME",
)

_missing_bucketeer_vars = [name for name in BUCKETEER_REQUIRED_VARS if not os.getenv(name)]
if _missing_bucketeer_vars:
    raise ImproperlyConfigured(
        "Production requires Bucketeer/S3 media storage. Missing config vars: "
        + ", ".join(_missing_bucketeer_vars)
    )

AWS_ACCESS_KEY_ID = os.environ["BUCKETEER_AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["BUCKETEER_AWS_SECRET_ACCESS_KEY"]
AWS_S3_REGION_NAME = os.environ["BUCKETEER_AWS_REGION"]
AWS_STORAGE_BUCKET_NAME = os.environ["BUCKETEER_BUCKET_NAME"]

# Bucketeer documents public objects under the public/ prefix. Keep every Django
# media upload there so images/documents from admin and imported legacy assets
# are durable and directly readable by the frontend.
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_USE_SSL = True
AWS_S3_VERIFY = True
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_ADDRESSING_STYLE = "virtual"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "location": "public",
            "default_acl": None,
            "file_overwrite": False,
            "querystring_auth": False,
            "object_parameters": AWS_S3_OBJECT_PARAMETERS,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/public/"
