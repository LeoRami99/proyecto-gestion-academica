import pymsql

def obtener_conexion():
    return pymsql.connect(
        host='localhost',
        user='root',
        password = '',
        db='prueba',
    )