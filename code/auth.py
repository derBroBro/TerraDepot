import json
import logging
import os
import base64
from lib import create_response, randomString, write_key, read_key_or_default, get_config

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))

KEY = os.environ.get("KEY")


def lambda_handler(event, context):


    logger.info(event)
    logger.info(context)

    # decode user and password
    if not "Authorization" in event["headers"]:
        return create_policy("NONE", "Deny")
    auth_raw = event["headers"]["Authorization"].split(" ")[1]
    auth_obj = base64.b64decode(auth_raw).decode("utf-8").split(":")
    auth_user = auth_obj[0]
    auth_pass = auth_obj[1]

    arn = event["methodArn"]
    logger.info(f"Got auth request from {auth_user} for {arn}")

    # if a new reuqest, use the global key (TBD restrict the cli to the token)
    if auth_user == "admin":
        logger.info("Got request for admin")
        if auth_pass == KEY:
            logger.info("PW correct allow usage of new")
            return create_policy(auth_user, arn, "Allow")
        else:
            logger.warn("Admin key does not fit, reject")
            raise Exception('Unauthorized')

    # for state or info use the key from the project
    if event["resource"] == "/project/{projectId}/terraform.tfstate":
        logger.info("Got request for info or state")
        if auth_user == "token":
            project_id = event["pathParameters"]["projectId"]    
            logger.info(f"Got request for project {project_id}")
            config = get_config(project_id)
            project_name = config["name"]
            project_token = config["token"]
            logger.info(f"Got request for {project_name} with id {project_id}")
            if project_token == auth_pass:
                logger.info("Token fits the project ones, allow")
                return create_policy(project_id, arn, "Allow")
            else:
                logger.warn("Token does not fit, reject")
                raise Exception('Unauthorized')

    logger.error("Got invalid request, Deny")
    raise Exception('Unauthorized')

   

def create_policy(principalId, apiArn, effect="Deny"):
    policy = {
        "principalId": principalId,
        "policyDocument": {
            "Version": '2012-10-17',
            "Statement": [
                {
                    "Action": 'execute-api:Invoke',
                    "Effect": effect,
                    "Resource": [apiArn]
                }
            ]
        }
    }
    logger.info(policy)
    return policy