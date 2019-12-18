import json
import logging
import os
import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))

BUCKET = os.environ.get('S3_BUCKET')
    
s3_client = boto3.resource('s3')


def create_response(body, code=200, contenttype="application/json"):
    logger.info(f"{code} --> {body}")
    return {
        "statusCode": code,
        "body": body,
        "headers": {
            "Content-Type": contenttype,
        }
    }


def lambda_handler(event, context):
    ### Auth here
    
    logger.info(event)

    ## fix is not there
    project_id = event["pathParameters"]["projectId"]    
    logger.info(f"Got request for project {project_id}")

    configfile = f"{project_id}/config.json"
    statefile = f"{project_id}/terraform.tfstate"

    
    config = json.loads(read_key_or_default(configfile))
    project_name = config["name"]
    logger.info(f"Got request for {project_name} with id {project_id}")


    self_url = "https://" + event["requestContext"]["domainName"]

    # Get existing state or create new
    if event['httpMethod'] == "GET":
        logger.info("Type is GET, send state")
        data = read_key_or_default(statefile)
        if data == None:
            return create_response(f"No project exists, please visit {self_url}/project/new")
        else:
            return create_response(data.decode('utf-8'))
        
    # update
    if event['httpMethod'] == "POST":
        logger.info("Type is POST, save and send state")
        data = read_key_or_default(configfile)
        if data == None:
            return create_response(f"No project exists, please visit {self_url}/project/new")
        else:
            data = event["body"]
            write_key(statefile,data)
            return create_response(data)

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