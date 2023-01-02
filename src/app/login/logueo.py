from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from conection_mysql import obtener_conexion
conn = obtener_conexion()
class Usuario(UserMixin):
    def __init__(self, id, nombre_usuario, contrasena, rol="", nombre="", apellido=""):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.rol = rol
        self.nombre = nombre
        self.apellido = apellido
    def login(self, conexion):
        cursor = conexion.cursor()
        sql="SELECT * FROM admin_academico WHERE nombre_usuario='{0}' ".format(self.nombre_usuario)
        cursor.execute(sql)
        fila=cursor.fetchone()
        if fila !=None:
            usuario= Usuario(fila[0], fila[1], check_password_hash(fila[5], self.contrasena), fila[8] ,fila[2], fila[3])
            return usuario
        else:
            return None
    @classmethod
    def obtener_usuario(self, id):
        cursor = conn.cursor()
        sql="SELECT id, nombre_usuario, password, rol, nombre, apellido FROM admin_academico WHERE id={0}".format(id)
        cursor.execute(sql)
        print('SQL: ', sql)
        fila=cursor.fetchone()
        print('Fila: ', fila)
        if fila !=None:
            usuario= Usuario(fila[0], fila[1], None, fila[3], fila[4], fila[5])
            return usuario
        else:
            return None
