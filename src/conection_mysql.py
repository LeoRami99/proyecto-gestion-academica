import pymysql 
host = "localhost"
user = "root"
password = "root"
db = "proyecto"
def conection():
    try:
        con = pymysql.connect(host, user, password, db)
        return con
    except:
        return("Error de conexion")