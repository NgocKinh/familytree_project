import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",             # thay user MySQL
        password="Msand@167",# thay mật khẩu
        database="familytreedb"
    )
