import json
import logging
import os
import boto3
import botocore
import random
import string

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))

BUCKET = os.environ.get('S3_BUCKET')
DOMAIN = os.environ.get('DOMAIN')

DEFAULT_STATE = ""
with open("default.tfstate.template", "r") as file:
    DEFAULT_STATE = file.read()
    
NEW_FORM = ""
with open("new_project_form.html", "r") as file:
    NEW_FORM = file.read()
    
HELP = ""
with open("new_project_created.html", "r") as file:
    HELP = file.read()

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

def lambda_handler(event, context):    
    # Get existing state or create new
    if event['httpMethod'] == "GET":
        logger.info(f"Send form for creation")
        return create_response(NEW_FORM,contenttype="text/html")
        
    # update
    if event['httpMethod'] == "POST":
        body_vars = {}
        body = event["body"]
        for line in body.split("\n"):
            line_data = line.split("=")
            body_vars[line_data[0]]=line_data[1]

        name = body_vars["name"]
        project_id = randomString(48)
        config = json.dumps({"name":name})

        logger.info("Create project {name} with id {project_id}")
        
        write_key(f"{project_id}/config.json",config)
        write_key(f"{project_id}/terraform.tfstate",DEFAULT_STATE)
        
        demo_state_template = """terraform {{
    backend "http" {{
        address = "https://{0}/project/{1}/terraform.tfstate"
    }}
}}
"""
        demo_state = demo_state_template.format(DOMAIN,project_id)
        output = HELP.replace("###STATE###",demo_state)
        return create_response(output,contenttype="text/html")

def write_key(filename, data):
    logger.info(f"write file {filename} to {BUCKET}")
    s3_obj = s3_client.Object(BUCKET, filename)
    s3_obj.put(Body=data) 