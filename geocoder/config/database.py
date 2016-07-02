import sqlite3

import psycopg2
import yaml


REQUIRED_SQLITE_FIELDS = ('database',)
REQUIRED_POSTGRES_FIELDS = ('database', 'host', 'port', 'user', 'password')


def read_config(config_file):
    config = yaml.load(config_file)
    if 'dialect' not in config:
        raise ValueError("config must contain 'dialect' field")
    if config['dialect'] == 'postgresql':
        dialect = psycopg2
        if not all(field in config for field in REQUIRED_POSTGRES_FIELDS):
            raise ValueError("postgres config objects must have at least the "
                             "following fields: {}".format(
                             ', '.join(REQUIRED_POSTGRES_FIELDS)))
    elif config['dialect'] == 'sqlite':
        dialect = sqlite3
        if not all(field in config for field in REQUIRED_SQLITE_FIELDS):
            raise ValueError("sqlite config objects must have at least the "
                             "following fields: {}".format(
                             ', '.join(REQUIRED_SQLITE_FIELDS)))
    else:
        raise NotImplementedError

    del config['dialect']
    return dialect, config
