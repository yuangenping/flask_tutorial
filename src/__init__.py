import os
from . import context_processor, app_cfg
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=os.getenv("SECRET_KEY"))
    app.config.from_object(app_cfg.BaseConfig(app))

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

    from . import user, blog, index, html_filter, context_processor, error_handler
    from .models.extensions import db
    from .models.user import User
    from .models.blog import Blog

    # db.init_app(app)
    html_filter.init(app)
    context_processor.init(app)
    error_handler.init(app)

    app.register_blueprint(index.index_bp)
    app.register_blueprint(user.user_bp)
    app.register_blueprint(blog.blog_bp)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
