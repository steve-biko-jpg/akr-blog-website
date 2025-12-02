import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="STeVe!@a#kr5239",
        database="akrblog",
        cursorclass=pymysql.cursors.DictCursor
    )
