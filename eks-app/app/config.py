import os

DATABASE_URL = os.getenv("DATABASE_URL")
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

if not S3_BUCKET:
    raise ValueError("S3_BUCKET not set")
