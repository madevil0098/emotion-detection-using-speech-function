import pymysql
from pymysql.cursors import DictCursor

def getConnection():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                             user='root', 
                             password='1234',
                             database='smarteye',
                             cursorclass=DictCursor)
    return connection                             
