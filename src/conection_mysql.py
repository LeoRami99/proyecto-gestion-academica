from pymysql import connect

def obtener_conexion():
    try:
        conn = connect(host ='localhost', user='root', password='', db='gestionacademico_app')
        return conn
    except Exception as e:
        print(e)
        return None