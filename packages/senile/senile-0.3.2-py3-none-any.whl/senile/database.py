"""
Database connection.
"""
import logging
import os
import sqlite3
import sys

db_type = os.getenv('SENILE_DB_TYPE', 'sqlite3')
db_path = os.path.expanduser(
        os.getenv('SENILE_DB_PATH', '~/.senile')
        )
logger = logging.getLogger(__name__)

CREATE_TABLES=[
    '''
    CREATE TABLE IF NOT EXISTS tasks (
        uuid TEXT NOT NULL PRIMARY KEY,
        id INTEGER NOT NULL,
        text TEXT NOT NULL,
        priority INTEGER NOT NULL DEFAULT 1,
        status INTEGER NOT NULL,
        created_time REAL NOT NULL,
        modified_time REAL NOT NULL,
        start_time REAL NOT NULL,
        done_time REAL NOT NULL,
        duration REAL NOT NULL,
        notes TEXT NOT NULL DEFAULT ""
        );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS task_tags (
        task_id TEXT NOT NULL,
        tag TEXT NOT NULL,
        CONSTRAINT unique__task_id__tag UNIQUE(task_id, tag)
    );
    '''
]

def execute(query, args=[]):
    "Execute a query on the database."
    if db_type == 'sqlite3':
        if not os.path.isdir(os.path.dirname(db_path)):
            db_dir = os.path.dirname(db_path)
            logger.info("Creating database directory '{}'.".format(db_dir))
            os.makedirs(db_dir)
        if not os.path.isfile(db_path):
            logger.info("Initiating sqlite3 database in '{}'.".format(db_path))
            with sqlite3.connect(db_path) as con:
                cur = con.cursor()
                for sql in CREATE_TABLES:
                    cur.execute(sql)
        data = None
        with sqlite3.connect(db_path) as con:
            con.set_trace_callback(logger.info)
            cur = con.cursor()
            cur.execute(query, args)
            data = cur.fetchall()
        return data
    else: # pragma: no cover
        logger.error('{} database not implemented yet.'.format(db_type))
        return None

