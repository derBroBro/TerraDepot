import json
import logging
import os
import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))

BUCKET = os.environ.get('S3_BUCKET')
DEFAULT_STATE = ""
with open("default.tfstate.template", "r") as file:
    DEFAULT_STATE = file.read()
    
s3_client = boto3.resource('s3')


def create_response(body, code=200):
    logger.info(f"{code} --> {body}")
    return {
        "statusCode": code,
        "body": body.decode('utf-8')
    }

def lambda_handler(event, context):
    ### Auth here
    
    logger.info(event)

    ## fix is not there
    project_id = event["pathParameters"]["projectId"]

    # Check if key available
    try:
        key = event["queryStringParameters"]["key"]
    except (KeyError, TypeError):
        return create_response("Access denied, no key provided", 403)
    
    logger.info(f"Got request for project {project_id}")

    configfile = f"{project_id}/config.json"
    statefile = f"{project_id}/terraform.tfstate"

    config_str = get_key_or_default(configfile,"NONE")

    # Get existing state or create new
    if event['httpMethod'] == "GET":
        # check if the state already exists
        if config_str == "NONE":
            # if not, save the inital key
            logger.warn(f"No config found, write default with key {key}")
            write_key(configfile,json.dumps({"key":key}))
        else: 
            config = json.loads(config_str)
            # else, check if the key is as defined
            if config["key"] != key:
                return create_response("Access denied, Key wrong!", 403)
        data = get_key_or_default(statefile,DEFAULT_STATE)
        return create_response(data)
        
    # update
    if event['httpMethod'] == "POST":
        # check of config available
        if config_str == "NONE":
            # if not, break
            return create_response("Access denied, not key defined in state. This is an unexpected behavoir!", 500)
        else: 
            config = json.loads(config_str)
            # else, check if the key is as defined
            if config["key"] != key:
                return create_response("Access denied, key wrong!", 403)
        if not "body" in event:
            return create_response("Empty body!", 500)
        data = event["body"]
        write_key(statefile,data)
        return create_response(data)

def write_key(filename, data):
    logger.info(f"write file {filename} to {BUCKET}")
    s3_obj = s3_client.Object(BUCKET, filename)
    s3_obj.put(Body=data) 

def get_key_or_default(filename, default_value):
    logger.info(f"read file {filename} to {BUCKET}")
    s3_obj = s3_client.Object(BUCKET, filename)
    try:
        data = s3_obj.get()["Body"].read()
        return data
    # make nicer and chat execption
    except botocore.exceptions.ClientError as e:
        logger.warn(f"No file yet, send default value ({default_value})")
        return default_value