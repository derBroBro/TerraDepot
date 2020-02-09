import importlib
import logging
from .lib import *

logger = logging.getLogger()


def run(resource):
    try:
        res_type = resource["type"]
        logger.info(f"Try to find check for {res_type}")
        resource_checker = importlib.import_module(f"check_costs.res.{res_type}")
        return resource_checker.run(resource)
    except Exception:
        logger.warn(f"No checker found, skip")
        return None
