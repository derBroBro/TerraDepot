import logging
import os
import json
from jinja2 import Template
from lib import (
    create_response,
    read_key_or_default,
    read_file,
    get_tf_res,
    get_tf_metadata,
    get_config,
    render_template,
)

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

TEMPLATE_FILE = "templates/project_info.html"
DOMAIN = os.environ.get("DOMAIN")


def lambda_handler(event, context):
    project_id = event["pathParameters"]["projectId"]
    logger.info(f"Got request for project {project_id}")

    report_path = f"{project_id}/report.json"

    report = json.loads(read_key_or_default(report_path, "{}"))
    if not "metadata" in report:
        return create_response(
            "No report is available (yet). Please check out in a view seconds.",
            code=404,
        )

    # Get existing state or create new
    if event["httpMethod"] == "GET":
        output = render_template(
            template_file=TEMPLATE_FILE,
            report=report,
            project_id=project_id,
            domain=DOMAIN,
        )
        return create_response(output, contenttype="text/html")
