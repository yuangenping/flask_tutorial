import os


class BaseConfig(object):

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        print("获取配置: DATABASE")
        return f"sqlite:///{os.path.join(self.app.instance_path, "src.sqlite")}"

    def __init__(self, app):
        self.app = app
