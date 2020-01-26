import boto3
import os
from moto import mock_s3

os.environ["S3_BUCKET"] = "test-bucket"
os.environ["DOMAIN"] = "test.local"
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_SECURITY_TOKEN'] = 'testing'
os.environ['AWS_SESSION_TOKEN'] = 'testing'

@mock_s3
def setup_s3():
    conn = boto3.resource("s3")
    conn.create_bucket(Bucket=os.environ["S3_BUCKET"])

if __name__ == "__main__":
    setup_s3()
    test = os.environ["S3_BUCKET"]
    print(test)
    