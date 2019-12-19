import json
import logging
import os
import urllib.parse
from lib import create_response, randomString, write_key, read_file,redirect

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))

DOMAIN = os.environ.get('DOMAIN')

DEFAULT_STATE = read_file("templates/default.tfstate.template")
PROJECT_FORM = read_file("templates/project_form.html")

def lambda_handler(event, context):    
    # Get existing state or create new
    if event['httpMethod'] == "GET":
        logger.info(f"Send form for creation")
        return create_response(PROJECT_FORM,contenttype="text/html")
        
    # update
    if event['httpMethod'] == "POST":
        body_vars = {}
        body = urllib.parse.unquote(event["body"])
        for line in body.split("&"):
            line_data = line.split("=")
            body_vars[line_data[0]]=line_data[1]

        logger.info(body_vars)
        logger.info("name" in body_vars)
        logger.info("owner" in body_vars)
        if not ("name" in body_vars and "owner" in body_vars):
            return create_response("Missing field owner or name",code=500)

        name = body_vars["name"]
        owner = body_vars["owner"]
        project_id = randomString(48)
        config = json.dumps({"name":name, "owner":owner})

        logger.info(f"Create project {name} with id {project_id}")
        
        write_key(f"{project_id}/config.json",config)
        write_key(f"{project_id}/terraform.tfstate",DEFAULT_STATE)
        
        return redirect(f"https://{DOMAIN}/project/{project_id}/info")

