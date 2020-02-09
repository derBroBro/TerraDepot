from enum import Enum


def gen_review(tests):
    final_state = -1
    for test in tests:
        if test["state"] > final_state:
            final_state = test["state"]
    return {"state": final_state, "tests": tests}


def get_test(state, message):
    result = {"state": state.value, "message": message}
    return result


class STATE(Enum):
    UNKNOWN = -1
    OK = 0
    WARNING = 1
    CRITICAL = 2
