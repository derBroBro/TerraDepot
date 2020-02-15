import logging
import os
import json
from jinja2 import Template
from lib import (
    create_response,
    get_reports,
    render_template
)

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

DOMAIN = os.environ.get("DOMAIN")


def lambda_handler(event, context):
    logger.info(f"Got request for listing projects")

    reports = get_reports()

    # Get existing state or create new
    if event["httpMethod"] == "GET":
        output = render_template(
            template_file="project_list.html",
            reports=reports,
            domain=DOMAIN,
        )
        return create_response(output, contenttype="text/html")
