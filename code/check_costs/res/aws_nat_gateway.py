from ..lib import get_montly_costs

def run(resource):
    # eu-central-1, 0,052 USD/h
    return get_montly_costs(0.052,"h")