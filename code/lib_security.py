def get_security(resource):
    # -1 unknown
    # 0 ok
    # 1 warning
    # 2 critical
    # 3 empty (missing ressource)
    if resource["type"] == "aws_s3_bucket":
        if len(resource["instances"]) == 0:
            return 3

        for i in resource["instances"]:
            if len(i["attributes"]["logging"]) == 0:
                return 2
        return 0

    return -1