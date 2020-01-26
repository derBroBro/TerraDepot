import json
import logging
import os
import urllib.parse
from jinja2 import Template
from lib import create_response, randomString, write_key, read_file, redirect, get_post_parameter, new_project

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))

DOMAIN = os.environ.get('DOMAIN')
KEY = os.environ.get('KEY')

PROJECT_FORM = read_file("templates/project_form.html")


def lambda_handler(event, context):

    # Get existing state or create new
    if event['httpMethod'] == "GET":
        logger.info(f"Send form for creation")
        return create_response(PROJECT_FORM,contenttype="text/html")
        
    # update
    if event['httpMethod'] == "POST":
        body_vars = get_post_parameter(event)
        if not ("name" in body_vars and "owner" in body_vars and "token" in body_vars):
            return create_response("Missing field owner, name or token",code=500)

        project_id = new_project(body_vars["name"], body_vars["owner"], body_vars["token"] )
        
        return redirect(f"https://{DOMAIN}/project/{project_id}/info")

