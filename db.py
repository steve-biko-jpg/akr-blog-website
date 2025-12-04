import os
import pymysql

def get_connection():
    return pymysql.connect(
        host=os.environ.get("MYSQLHOST", "localhost"),       # Render host or default localhost
        user=os.environ.get("MYSQLUSER", "root"),           # Render user or local user
        password=os.environ.get("MYSQLPASSWORD", "STeVe!@a#kr5239"),   # Render password or local password
        database=os.environ.get("MYSQLDATABASE", "akrblog"),    # Render database or local db
        cursorclass=pymysql.cursors.DictCursor
    )
