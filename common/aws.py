from os.path import basename, splitext
import uuid
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from config.settings import (
    AWS_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
    AWS_STORAGE_TEMP_BUCKET_NAME,
    SIGNATURE_VERSION,
)

# AWS config
SIGNATURE_VERSION = SIGNATURE_VERSION
AWS_REGION = AWS_REGION
AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
AWS_STORAGE_TEMP_BUCKET_NAME = AWS_STORAGE_TEMP_BUCKET_NAME


def create_unique_filename(filename):
    base = basename(filename)
    _, extension = splitext(base)
    unique = uuid.uuid4().hex
    return f"{unique}{extension}"


def extract_file_name(url):
    marked = url.find("?")

    if marked > -1:
        washed = url[: url.find("?")]
        return basename(washed)
    else:
        return basename(url)


def create_s3_client():
    return boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(SIGNATURE_VERSION),
    )


def create_s3_resource():
    return boto3.resource(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(SIGNATURE_VERSION),
    )


def s3_file_exists(bucket, key):
    try:
        create_s3_client().head_object(
            Bucket=bucket,
            Key=key,
        )
        return True
    except ClientError:
        return False


def s3_move_temp_file(filename, to_folder):
    """s3 파일 복사 temp_bucket -> live_bucket"""

    to_key = f"{to_folder}{filename}"
    s3_resource = create_s3_resource()

    try:
        # copy
        s3_resource.Object(AWS_STORAGE_BUCKET_NAME, f"{to_key}",).copy_from(
            CopySource=f"{AWS_STORAGE_TEMP_BUCKET_NAME}/{filename}",
            # ACL="public-read",
        )
        # delete
        # s3_resource.Object(
        #     settings.AWS_TEMPORARY_BUCKET_NAME,
        #     from_key,
        # ).delete()
        return True, to_key
    except ClientError as eee:
        print(str(eee))
        return False, None


def s3_delete_file(folder, filename):
    """s3 파일 삭제"""
    s3_resource = create_s3_resource()

    s3_resource.Object(
        AWS_STORAGE_BUCKET_NAME,
        f"{folder}{filename}",
    ).delete()


def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method, Params=method_parameters, ExpiresIn=expires_in
        )

    except ClientError:
        raise
    return url


def create_presigned_url(key):
    s3_client = create_s3_client()
    client_action = "put_object"

    put_url = generate_presigned_url(
        s3_client,
        client_action,
        {
            "Bucket": AWS_STORAGE_TEMP_BUCKET_NAME,
            "Key": key,
        },
        180,
    )
    return put_url


def get_s3_obj_list():
    """S3 파일 목록 가져오기"""
    s3 = create_s3_resource()
    my_bucket = s3.Bucket(AWS_STORAGE_TEMP_BUCKET_NAME)
    obj_list = [i.key for i in my_bucket.objects.all()]

    return obj_list
