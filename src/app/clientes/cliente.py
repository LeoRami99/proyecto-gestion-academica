from datetime import datetime
from conection_mysql import obtener_conexion
class Cliente():
    def __init__(self, codigo_cliente, nombre_cliente):
        self.codigo_cliente = codigo_cliente
        self.nombre_cliente = nombre_cliente
        
    def guardar_cliente(self):
        # Si la conexión no se hace mostrar en pantalla el error
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "INSERT INTO cliente (codigo_cliente, nombre_cliente) VALUES ('{0}', '{1}')".format(self.codigo_cliente, self.nombre_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
            
      