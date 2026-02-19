import boto3
from .config import S3_BUCKET, AWS_REGION

s3 = boto3.client("s3", region_name=AWS_REGION)

def upload_file(file_obj, key):
    s3.upload_fileobj(file_obj, S3_BUCKET, key)

def generate_presigned_url(key: str):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": key},
        ExpiresIn=3600
    )
