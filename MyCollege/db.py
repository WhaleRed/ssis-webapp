import psycopg2
from flask import g
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=DB_NAME,
            user= DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            sslmode='require'
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()