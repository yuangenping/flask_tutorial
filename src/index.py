from flask import (
    Blueprint,
    current_app,
    render_template,
    stream_template,
    Response,
    stream_with_context,
)
from flask.views import MethodView, View
import random
import time

index_bp = Blueprint("index", __name__, url_prefix="/index")


def read_log(lines):
    while lines > 0:
        time.sleep(0.2)
        yield random.randrange(0, 1000)
        lines -= 1


class CommonView(View):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def dispatch_request(self):
        return f"Hello,{self.name}"


class Index(MethodView):
    def get(self):
        current_app.logger.info("进入首页--->")
        return stream_template("index.html", logs=read_log(5))


index_bp.add_url_rule("", view_func=Index.as_view("index"))
index_bp.add_url_rule("/laowang", view_func=CommonView.as_view("laowang", "老王"))
index_bp.add_url_rule("/laozhang", view_func=CommonView.as_view("laozhang", "老张"))
