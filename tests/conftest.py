import sys
print("当前 sys.path:", sys.path)
import os
import tempfile
import pytest
from src import create_app
from src.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
     # 【前置准备 Setup】创建临时数据库，配置测试环境
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app # 【传递资源】把配置好的 app 交给测试函数使用

    # 【后置清理 Teardown】测试跑完后，自动删除临时数据库文件
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/user/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/user/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)