import json
import logging
import os
from jinja2 import Template
from lib import create_response, randomString, write_key, read_file

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))

DOMAIN = os.environ.get('DOMAIN')

DEFAULT_STATE = read_file("templates/default.tfstate.template")
PROJECT_FORM = read_file("templates/project_form.html")
PROJECT_CREATED = read_file("templates/project_created.html")
PROJECT_CREATED_TEMPLATE = Template(PROJECT_CREATED)

def lambda_handler(event, context):    
    # Get existing state or create new
    if event['httpMethod'] == "GET":
        logger.info(f"Send form for creation")
        return create_response(PROJECT_FORM,contenttype="text/html")
        
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
        
        output = PROJECT_CREATED_TEMPLATE.render(domain=DOMAIN, id=project_id)
        return create_response(output,contenttype="text/html")

