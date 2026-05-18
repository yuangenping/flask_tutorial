from .extensions import db
import time


class Blog(db.Model):
    __tablename__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False, comment="创建人id")
    created = db.Column(db.DateTime, nullable=False, default=time.time(), comment="创建时间")
    title = db.Column(db.String(50), nullable=False, unique=True, comment="标题")
    body = db.Column(db.String(1000), nullable=False, comment="内容")
