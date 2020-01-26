import random
import string
import logging
import boto3
import botocore
import os
import json
import urllib.parse
from lib_costs import get_costs
from lib_security import get_security

logger = logging.getLogger()

BUCKET = os.environ.get('S3_BUCKET')
DEFAULT_STATE = "templates/default.tfstate.template"

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
def redirect(url):
    logger.info(f"Redirect to {url}")
    return {
        "statusCode": 301,
        "body": "body",
        "headers": {
            "Location": url,
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
        if not default_value == None:
            default_value = default_value.encode("UTF8")
        return default_value

def read_file(filename):
    with open(filename, "r") as file:
        return file.read()

def get_tf_res(tf_state):
    result = []
    resources = tf_state["resources"]
    for res in resources:
        if res["mode"] == "managed":
            name = res["name"]

            if "module" in res:
                mod = res["module"]
                res["id"] = f"{mod}.{name}"
            else:
                res["id"] = name    
                
            # get costs
            res["costs"] = get_costs(res)
            res["security"] = get_security(res)

            result.append(res)

    return result

def get_tf_metadata(tf_state):
    version = 0
    terraform_version = 0
    serial = 0

    if "version" in tf_state:
        version = tf_state["version"]
    if "terraform_version" in tf_state:
        terraform_version = tf_state["terraform_version"]
    if "serial" in tf_state:
        serial = tf_state["serial"]

    return {
        "version": version,
        "terraform_version": terraform_version,
        "serial": serial
    }

def get_post_parameter(event):
    body_vars = {}
    if not "body" in event:
        return body_vars
    
    body = urllib.parse.unquote(event["body"])
    for line in body.split("&"):
        line_data = line.split("=")
        body_vars[line_data[0]]=line_data[1]
    return body_vars

def new_project(name, owner, token):
    project_id = randomString(48)
    config = json.dumps({"name":name, "owner":owner, "token":token})
    state = read_file(DEFAULT_STATE)

    logger.info(f"Create project {name} with id {project_id}")
        
    write_key(f"{project_id}/config.json",config)
    write_key(f"{project_id}/terraform.tfstate",state)

    return project_id

def get_config(project_id):
    raw_data = read_key_or_default(f"{project_id}/config.json", "{\"name\":\"invalid\",\"token\":\"invalid\",\"owner\":\"invalid\"}")
    return json.loads(raw_data)
        


    
