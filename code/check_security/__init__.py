import importlib
import logging
from .lib import *

logger = logging.getLogger()

def run(resource):
    tests = []
    try:
        res_type = resource["type"]
        logger.info(f"Try to find check for {res_type}")
        resource_checker = importlib.import_module(f"check_security.res.{res_type}")
        tests = resource_checker.run(resource)
    except Exception:
        logger.warn(f"No checker found, skip")

    return gen_review(tests)