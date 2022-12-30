from werzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from conection_mysql import *
class UsuariosAdmins():
  def __init__(self, id, usuario, password):
    self.id = id
    self.usuario = usuario
    self.password = password

  def obtener_usuario(self, id):
    con = conection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios_admins WHERE id = %s", (id))
    usuario = cursor.fetchone()
    return UsuariosAdmins(usuario[0], usuario[1], usuario[2])