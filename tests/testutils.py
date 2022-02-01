import json

FILEPATH_JSON = 'expected_json/'
FILEPATH_TESTS_JSON = 'tests/expected_json/'


def import_json(filename):
    # Find JSON assuming "tests" is the current working directory
    try:
        with open(f"{FILEPATH_JSON}{filename}", 'r') as file:
            data = json.load(file)
    # Could not find file, thus assume the current working dir is "blog_posts"
    except FileNotFoundError:
        with open(f"{FILEPATH_TESTS_JSON}{filename}", 'r') as file:
            data = json.load(file)
    return data
