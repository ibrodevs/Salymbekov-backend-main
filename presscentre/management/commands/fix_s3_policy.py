from django.core.management.base import BaseCommand
import boto3
import json
from django.conf import settings


class Command(BaseCommand):
    help = 'Fix S3 bucket policy for public read access'

    def handle(self, *args, **options):
        if not all([
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
            settings.AWS_STORAGE_BUCKET_NAME,
            settings.AWS_S3_REGION_NAME
        ]):
            self.stdout.write(
                self.style.WARNING('S3 settings not configured. Skipping bucket policy setup.')
            )
            return

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        # First, try to disable Block Public Access settings
        try:
            s3_client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully disabled Block Public Access for bucket {bucket_name}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not modify Block Public Access settings: {e}')
            )

        # Set bucket policy for public read access
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        try:
            s3_client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(bucket_policy)
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully set public read policy for bucket {bucket_name}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to set bucket policy: {e}')
            )