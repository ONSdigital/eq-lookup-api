import os

def get_env_or_fail(key):
    value = os.getenv(key)
    if value is None:
        raise Exception("Setting '{}' Missing".format(key))

    return value

LOOKUP_URL = get_env_or_fail('LOOKUP_URL')