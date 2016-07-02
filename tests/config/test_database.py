from __future__ import unicode_literals

import io
import sqlite3
import textwrap

import psycopg2

from geocoder.config import database


def test_postgres_config():
    config = textwrap.dedent("""
        dialect: postgresql
        database: testdb
        host: postgres.whatever.com
        port: 5432
        user: kevin
        password: secret
    """)

    config_io = io.StringIO(config)
    dialect, config_dict = database.read_config(config_io)
    assert set(config_dict.keys()) == {'database', 'host', 'port', 'user', 'password'}
    assert dialect is psycopg2
    assert config_dict['database'] == 'testdb'
    assert config_dict['host'] == 'postgres.whatever.com'
    assert config_dict['port'] == 5432
    assert config_dict['user'] == 'kevin'
    assert config_dict['password'] == 'secret'


def test_sqlite_config():
    config = textwrap.dedent("""
        dialect: sqlite
        database: testdb.db
    """)

    config_io = io.StringIO(config)
    dialect, config_dict = database.read_config(config_io)
    assert set(config_dict.keys()) == {'database'}
    assert dialect is sqlite3
    assert config_dict['database'] == 'testdb.db'
