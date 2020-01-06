def get_montly_costs(price, intervall):
    if intervall == "d": 
        return price*30
    if intervall == "h": 
        return get_montly_costs(price*24,"d")
    if intervall == "m":
        return get_montly_costs(price*60,"h")
    if intervall == "s":
        return get_montly_costs(price*60,"m")
    return -1


def get_costs(resource):
    if resource["type"] == "aws_nat_gateway":
        # eu-central-1, 0,052 USD/h
        return get_montly_costs(0.052,"h")

    if resource["type"] == "aws_kms_key":
        # 1USD/mon
        return 1.0
    return None