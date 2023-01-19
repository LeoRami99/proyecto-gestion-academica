from conection_mysql import obtener_conexion
# importación de seguridad de contraseña
from werkzeug.security import generate_password_hash, check_password_hash


class Admin():
    def __init__(self, nombre_usuario=None, contrasena=None, nombre=None, apellido=None, email=None, telefono=None, rol=None, cliente=None):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.cliente = cliente
        self.rol = rol

    @classmethod
    def obtener_usernames(self, nombre_usuario):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT nombre_usuario FROM usuarios WHERE nombre_usuario = '{0}'".format(nombre_usuario)
            cursor.execute(sql)
            username = cursor.fetchone()
            if username:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
    
    def registrar_administrador(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "INSERT INTO usuarios (nombre_usuario, nombre, apellido, correo, password, telefono, rol, estado, id_cliente) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(self.nombre_usuario, self.nombre, self.apellido, self.email, generate_password_hash(self.contrasena), self.telefono, self.rol, 1, self.cliente)
            print(sql)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    

