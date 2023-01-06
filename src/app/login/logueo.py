from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from conection_mysql import obtener_conexion
# Variable global para conexión a la base de datos
class Usuario(UserMixin):
    def __init__(self, id, nombre_usuario, contrasena, rol="", nombre="", apellido="", id_cliente=""):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.rol = rol
        self.nombre = nombre
        self.apellido = apellido
        self.id_cliente = id_cliente
    def login(self, conexion):
        try:
            conexion=obtener_conexion()
            cursor = conexion.cursor()
            sql="SELECT * FROM usuarios WHERE nombre_usuario='{0}' ".format(self.nombre_usuario)
            cursor.execute(sql)
            fila=cursor.fetchone()
            if fila !=  None:
                usuario = Usuario(fila[0], fila[1], check_password_hash(fila[5], self.contrasena), fila[8] ,fila[2], fila[3], fila[13])
                return usuario
            else:
                return None
        except Exception as e:
            print(e)
            return None
    @classmethod
    def obtener_usuario(self, id):
        try:
            conn= obtener_conexion()
            cursor = conn.cursor()
            sql="SELECT id, nombre_usuario, password, rol, nombre, apellido, id_cliente FROM usuarios WHERE id={0}".format(id)
            cursor.execute(sql)
            fila=cursor.fetchone()
            if fila != None:
                usuario = Usuario(fila[0], fila[1], None, fila[3], fila[4], fila[5], fila[6])
                return usuario
            else:
                return None
        except Exception as e:
            print(e)
            return None
            
    def id_nombreuser(nombre_usuario):
        try:
            conn= obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT id FROM usuarios WHERE nombre_usuario = '{0}'".format(nombre_usuario)
            cursor.execute(sql)
            fila = cursor.fetchone()
            if fila != None:
                return fila[0]
            else:
                return None
        except Exception as e:
            return None
