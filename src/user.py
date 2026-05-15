import functools

from flask import (
    current_app,
    Blueprint,
    jsonify,
    request,
    session,
    redirect,
    url_for,
    flash,
    render_template,
    g,
)
from flask.views import MethodView
from .db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.before_app_request
def log_logged_in_user():
    user_id = session.get("user_id")
    if not user_id:
        g.user = None
    else:
        user = (
            get_db()
            .execute(
                """
                    SELECT * FROM user where id = ?
                """,
                (user_id,),
            )
            .fetchone()
        )
        print(f"user--->{user}")
        g.user = user


def login_required(func):
    @functools.wraps(func)
    def warpper(*args, **kw):
        if not g.user:
            return redirect(url_for("user.login"))
        return func(*args, **kw)

    return warpper


class UserAPI(MethodView):

    def get(self):
        user_id = session.get("user_id", "未知用户")
        return f"获取的用户信息 id = {user_id}"

    def post(self):
        user_desc = request.json["userDesc"]
        if user_desc is None:
            return False
        return True

class UserLogoutApi(MethodView):
    def get(self):
        session.clear()
        return redirect(url_for('blog.index'))

class UserLoginApi(MethodView):
    def get(self):
        return render_template("user/login.html")

    def post(self):
        form_data = request.form
        user_name = form_data.get("username")
        password = form_data.get("password")
        if not user_name or not password:
            error = "userName or password is Required"
            return jsonify({"code": 400, "error": error}), 400
        db = get_db()
        user = db.execute(
            """
            SELECT * FROM user Where username = ?
            """,
            (user_name,),
        ).fetchone()
        if user is None:
            error = "not find user"
        elif not check_password_hash(user["password"], password):
            error = "password is error"
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("blog.index"))

        flash(error)
        return render_template("user/login.html")


class UserRegisterAPI(MethodView):

    def get(self):
        return render_template("user/register.html")

    def post(self):
        form_data = request.form
        error = None
        if not form_data or not form_data["userName"] or not form_data["password"]:
            error = "userName or password is Required"
            return jsonify({"code": 400, "error": error}), 400
        user_name = form_data["userName"]
        password = form_data["password"]
        db = get_db()
        try:
            db.execute(
                """
                INSERT INTO user(username,password) VALUES(?,?)            
            """,
                (user_name, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {user_name} is already registered."
        else:
            return redirect(url_for("user.login"))

        flash(error)

        return redirect(url_for("user.register"))


class UserTestRediectLogin(MethodView):

    decorators = [login_required]

    def get(self):
        pass


user_bp.add_url_rule("/", view_func=UserAPI.as_view("detail"))
user_bp.add_url_rule("/login", view_func=UserLoginApi.as_view("login"))
user_bp.add_url_rule("/logout", view_func=UserLogoutApi.as_view("logout"))
user_bp.add_url_rule("/register", view_func=UserRegisterAPI.as_view("register"))
user_bp.add_url_rule("/test", view_func=UserTestRediectLogin.as_view("test"))
