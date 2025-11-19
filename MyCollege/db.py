from flask import current_app, g
import psycopg2
from psycopg2 import pool

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(current_app.config['DB_CON_STR'])
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()