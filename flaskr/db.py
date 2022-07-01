import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool
from flask import g, current_app

load_dotenv()


def create_pool():
    DATABASE = os.getenv("DATABASE")
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

    return psycopg2.pool.SimpleConnectionPool(1, 10, database=DATABASE,
                                              user=DATABASE_USERNAME,
                                              password=DATABASE_PASSWORD)


def get_conn():
    if "conn" not in g:
        postgreSQL_pool = current_app.config["postgreSQL_pool"]
        g.conn = postgreSQL_pool.getconn()
    return g.conn


def close_conn(err):
    conn = g.pop("conn", None)

    if conn is not None:
        postgreSQL_pool = current_app.config["postgreSQL_pool"]
        postgreSQL_pool.putconn(conn)
