import logging
import os
import json
from jinja2 import Template
from lib import create_response, read_key_or_default, read_file, get_tf_res, get_tf_metadata

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))

INFO = read_file("templates/project_info.html")
INFO_TEMPLATE = Template(INFO)
DOMAIN = os.environ.get('DOMAIN')


def lambda_handler(event, context):
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
        config = json.loads(read_key_or_default(configfile))
        state = json.loads(read_key_or_default(statefile))
        if config == None:
            return create_response(f"No project exists, please visit {self_url}/project/new")
        else:
            metadata = get_tf_metadata(state)
            resources = get_tf_res(state)
            output = INFO_TEMPLATE.render(config=config, metadata=metadata, resources=resources, project_id=project_id, domain=DOMAIN )
            return create_response(output,contenttype="text/html")