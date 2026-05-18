from flask import Blueprint, render_template, stream_template, Response, stream_with_context
from flask.views import MethodView
import random
import time

index_bp = Blueprint("index", __name__, url_prefix="/index")

def read_log(lines):
    while lines > 0:
        time.sleep(0.2)
        yield random.randrange(0, 1000)
        lines -= 1


class Index(MethodView):
    def get(self):
        return stream_template("index.html", logs=read_log(5))


index_bp.add_url_rule("", view_func=Index.as_view("index"))
