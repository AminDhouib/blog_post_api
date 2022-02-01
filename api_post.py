import json
from flask import Flask, request
from flasgger import Swagger
from flasgger.utils import swag_from
from flasgger import LazyString, LazyJSONEncoder
import requests
from operator import itemgetter
import requests_cache
from enum import Enum
import threading

FAIL_CODE = 400


class SortBy(Enum):
    ID = "id"
    READS = "reads"
    LIKES = "likes"
    POPULARITY = "popularity"

    def __str__(self):
        return str(self.value)

    @staticmethod
    def from_str(label):
        if label == 'id':
            return SortBy.ID
        elif label == 'reads':
            return SortBy.READS
        elif label == 'likes':
            return SortBy.LIKES
        elif label == 'popularity':
            return SortBy.POPULARITY
        else:
            raise NotImplementedError


class Direction(Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self):
        return str(self.value)

    @staticmethod
    def from_str(label):
        if label in ('asc', 'ascending'):
            return Direction.ASC
        elif label in ('desc', 'descending'):
            return Direction.DESC
        else:
            raise NotImplementedError


class Thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name


def posts_remove_duplicates_id(posts_duplicates):
    posts_duplicates = sorted(posts_duplicates, key=itemgetter('id'))
    current_id = -1
    unique_posts = []
    for i in range(len(posts_duplicates)):
        if posts_duplicates[i]['id'] == current_id:
            pass  # do not append
        else:
            unique_posts.append(posts_duplicates[i])
            current_id = posts_duplicates[i]['id']
    return unique_posts


def get_post_from_tag(all_posts, lock, tag):
    url_request = "https://api.hatchways.io/assessment/blog/posts?tag=" + tag
    response = requests.get(url_request).json()
    with lock:
        for post in response["posts"]:
            all_posts.append(post)


def create_app():
    app = Flask(__name__)
    app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 3}
    requests_cache.install_cache('github_cache', backend='sqlite', expire_after=180)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/",
    }

    template = dict(
        swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
    )

    app.json_encoder = LazyJSONEncoder
    swagger = Swagger(app, config=swagger_config, template=template)

    @app.route("/")
    def index():
        return "Hello!"

    @app.route("/api/ping", methods=["GET"])
    @swag_from("swagger_ping_config.yml")
    def ping():
        return {"success": True}

    @app.route("/api/posts", methods=["GET"])
    @swag_from("swagger_posts_config.yml")
    def posts():
        tags = request.args.get("tags").lower().replace(',', ' ').split()

        # Check tags value
        if not tags:
            return {"error": "Tags parameter is required"}, FAIL_CODE

        # Check sortBy value
        try:
            sort_by = request.args.get("sortBy", default="id").lower()
            sort_by = str(SortBy.from_str(sort_by))
        except NotImplementedError:
            return {"error": "sortBy parameter is invalid"}, FAIL_CODE

        # Check direction value
        try:
            direction = request.args.get("direction", default="asc").lower()
            direction = Direction.from_str(direction)
        except NotImplementedError:
            return {"error": "direction parameter is invalid"}, FAIL_CODE

        # Get all posts from all tags (carrying duplicates for now)
        all_posts = []

        threads = []
        lock = threading.Lock()

        for tag in tags:
            threads.append(threading.Thread(
                target=get_post_from_tag,
                args=(all_posts, lock, tag,), ))

        # Start all threads
        for x in threads:
            x.start()

        # Wait for all of them to finish
        for x in threads:
            x.join()

        # Remove duplicates
        all_posts = posts_remove_duplicates_id(all_posts)

        # Sorting
        if direction is Direction.ASC:
            is_reverse = False
        else:
            is_reverse = True
        all_posts = sorted(all_posts, key=itemgetter(sort_by), reverse=is_reverse)

        # Format it to json and submit
        all_posts = {'posts': all_posts}
        return json.dumps(all_posts)

    @app.route("/square")
    def square():
        number = int(request.args.get("number", 0))
        return str(number ** 2)

    return app


if __name__ == "__main__":
    PORT_NUMBER = 5050
    doDebug = True
    app = create_app()
    app.run(debug=doDebug, port=PORT_NUMBER)
