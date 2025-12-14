import mysql.connector

def get_db_values():
    return mysql.connector.connect(
        host="localhost",
        port=3306,         
        user="root",
        password="root",
        database="instagram_clone"
    )
