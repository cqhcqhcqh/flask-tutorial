import sqlite3

import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # After the context, the connection should be closed.
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    # 如果上面的 sql 语句出现了带有 'closed' 信息的异常，表示 db 已经被关闭了
    # 如果不带 'closed' 信息的异常，说明 after app_context() 以后，the connection not be closed
    # 那么下面的 assert 就不会通过
    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    # 定义一个 Recorder class
    class Recorder(object):
        # 类属性？
        called = False
    
    # 定义一个 fake_init_db 方法
    def fake_init_db():
        Recorder.called = True

    # Use Pytest's monkeypatch fixture to replace the init_db function
    # with one the records that it's been called
    # 替换 flaskr.db.init_db 的默认实现为 fake_init_db（这个就相当是函数 IMP 的替换）
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    # runner 执行 `@click.command('init-db') def init_db` 方法，这个方法又会调用 db.init_db，所以最终又会调用 fake_init_db 方法
    result = runner.invoke(args=['init-db'])
    # `@click.command('init-db) def init_db ` 方法的最后一句是 click.echo('Initialized the database.')，这个 echo 的参数应该会给到 result.output
    assert 'Initialized' in result.output
    assert Recorder.called

