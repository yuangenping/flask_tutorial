from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    g,
    abort,
)

from flask.views import MethodView

from .db import get_db

from .user import login_required

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")


def get_blog_by_id(id: int):
    post = (
        get_db()
        .execute(
            """
            SELECT p.id ,
                p.title,
                p.body,
                p.created,
                p.author_id,
                u.username
                FROM post p 
                JOIN user u on p.author_id = u.id
                WHERE p.id = ?
                    """,
            (id,),
        )
        .fetchone()
    )
    return post


class Blog(MethodView):

    def get(self):
        db = get_db()
        posts = db.execute("""
                           SELECT p.id ,
                           p.title,
                           p.body,
                           p.created,
                           p.author_id,
                           u.username
                           FROM post p 
                           JOIN user u on p.author_id = u.id
                           ORDER BY p.created DESC
                           """).fetchall()
        return render_template("blog/index.html", posts=posts)


class BlogCreate(MethodView):

    decorators = [login_required]

    def get(self):
        return render_template("blog/create.html")

    def post(self):
        form_data = request.form
        error = ""
        title = form_data.get("title")
        body = form_data.get("body")
        if not title or not body:
            error = "标题和内容不能为空"
        else:
            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute(
                    """
                        INSERT INTO post(author_id,title,body) VALUES(?,?,?) 
                    """,
                    (g.user["id"], title, body),
                )
                db.commit()
                return redirect(url_for("blog.index"))
            except db.Error as e:
                error = "报错了"

        flash(error)

        return redirect(url_for("blog.create"))


class BlogUpdate(MethodView):
    def get(self, id: int):
        post = get_blog_by_id(id)
        if not post:
            abort(404, f"未找到文章")
        print(f"文章查询结果: {str(post)}")
        return render_template("blog/update.html", post=post)

    def post(self, id: int):
        form_data = request.form
        title = form_data.get("title")
        body = form_data.get("body")
        error = ""
        if not title or not body or not id:
            error = "未找到文章"
        else:
            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute(
                    """
                            UPDATE post set title = ?, body = ? where id = ?
                            """,
                    (title, body, id),
                )
                db.commit()
            except db.Error:
                error = "修改失败"

        flash(error)
        return redirect(url_for("blog.index"))


class BlogDelete(MethodView):
    def post(self):
        id = request.args.get("id")
        if not id and not isinstance(id, int):
            abort(400, "参数错误")
        post = get_blog_by_id(id)
        if not post:
            abort(404, "未找到blog")

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                           DELETE FROM post where id = ?
                           """,
                (id,),
            )
            db.commit()
        except db.Error:
            abort(500)

        return redirect(url_for("blog.index"))


blog_bp.add_url_rule("", view_func=Blog.as_view("index"))
blog_bp.add_url_rule("/create", view_func=BlogCreate.as_view("create"))
blog_bp.add_url_rule("/update/<int:id>", view_func=BlogUpdate.as_view("update"))
blog_bp.add_url_rule("/update", view_func=BlogUpdate.as_view("updatePost"))
blog_bp.add_url_rule("/delete", view_func=BlogDelete.as_view("delete"))
