def get_montly_costs(price, intervall):
    if intervall == "d":
        return price * 30
    if intervall == "h":
        return get_montly_costs(price * 24, "d")
    if intervall == "m":
        return get_montly_costs(price * 60, "h")
    if intervall == "s":
        return get_montly_costs(price * 60, "m")
    return -1
