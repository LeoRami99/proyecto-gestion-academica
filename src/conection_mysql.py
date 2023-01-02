from pymysql import connect

def obtener_conexion():
    return connect(
        host='localhost',
        user='root',
        password = '',
        db='gestionacademico_app',
    )