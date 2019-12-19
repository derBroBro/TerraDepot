import random
import string
import logging
import boto3
import botocore
import os

logger = logging.getLogger()

BUCKET = os.environ.get('S3_BUCKET')
s3_client = boto3.resource('s3')

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


def create_response(body, code=200, contenttype="application/json"):
    logger.info(f"{code} --> {body}")
    return {
        "statusCode": code,
        "body": body,
        "headers": {
            "Content-Type": contenttype,
        }
    }

def write_key(filename, data):
    logger.info(f"write file {filename} to {BUCKET}")
    s3_obj = s3_client.Object(BUCKET, filename)
    s3_obj.put(Body=data) 

def read_key_or_default(filename, default_value=None):
    logger.info(f"read file {filename} to {BUCKET}")
    s3_obj = s3_client.Object(BUCKET, filename)
    try:
        data = s3_obj.get()["Body"].read()
        return data
    # make nicer and chat execption
    except botocore.exceptions.ClientError as e:
        logger.warn(f"No file yet, send default value ({default_value})")
        return default_value

def read_file(filename):
    with open(filename, "r") as file:
        return file.read()

def get_tf_res():
    pass