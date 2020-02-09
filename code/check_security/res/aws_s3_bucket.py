from ..lib import STATE, get_test


def run(resource):
    tests = []
    if len(resource["instances"]) > 0:
        for i in resource["instances"]:
            if i["attributes"] != None:
                if len(i["attributes"]["logging"]) == 0:
                    tests.append(get_test(STATE.CRITICAL, "Logging disabled"))
                else:
                    tests.append(get_test(STATE.OK, "Logging enabled"))
    return tests
