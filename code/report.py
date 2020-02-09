import logging
import os
import json
from jinja2 import Template
from lib import create_response, read_key_or_default, get_tf_res, get_tf_metadata, get_config, gen_report, send_message

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL','INFO'))


def lambda_handler(event, context):
    CONFIG_TOPIC = os.environ["CONFIG_TOPIC"]
    STATE_TOPIC = os.environ["STATE_TOPIC"]
    DOMAIN = os.environ.get('DOMAIN')


    key = event["Records"][0]["s3"]["object"]["key"]
    project_id = key.split("/")[0]
    filename = key.split("/")[1]

    logger.info(f"Key is {key}")
    logger.info(f"project_id is {project_id}")
    logger.info(f"filename is {filename}")

    config = get_config(project_id)
    project_name = config["name"]

    if filename == "config.json":
        send_message(CONFIG_TOPIC, f"{project_name} with id {project_id} has been crete or updated", f"Project {project_name} update" )
    if filename == "terraform.tfstate":
        report = gen_report(project_id)
        if report["state"] > 1:
            send_message(STATE_TOPIC, f"{project_name} with id {project_id} has an critcal state, please check here https://{DOMAIN}/{project_id}/info", f"Project {project_name} has issues" )
        