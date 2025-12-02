import os
import pymysql

def get_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),       # Render host or default localhost
        user=os.environ.get("DB_USER", "root"),           # Render user or local user
        password=os.environ.get("DB_PASSWORD", "STeVe!@a#kr5239"),   # Render password or local password
        database=os.environ.get("DB_NAME", "akrblog"),    # Render database or local db
        cursorclass=pymysql.cursors.DictCursor
    )
