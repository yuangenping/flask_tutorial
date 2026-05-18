import os
from . import context_processor
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello World"

    from . import db, user, blog, index, html_filter, context_processor

    db.init_app(app)
    html_filter.init(app)
    context_processor.init(app)

    app.register_blueprint(index.index_bp)
    app.register_blueprint(user.user_bp)
    app.register_blueprint(blog.blog_bp)

    return app
