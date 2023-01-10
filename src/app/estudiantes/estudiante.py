from conection_mysql import obtener_conexion
""" 
  El tipo de documento se cambio directamente de int a varchar en la base de datos
 """
class Estudiante():
    def __init__(self, nombres=None, apellidos=None, tipo_doc=None, num_doc=None, correo=None, telefono=None, tel_fijo=None, ciudad=None, id_ciente=None, estado=None):
        self.nombres = nombres
        self.apellidos = apellidos
        self.tipo_doc = tipo_doc
        self.num_doc = num_doc
        self.correo = correo
        self.telefono = telefono
        self.tel_fijo = tel_fijo
        self.ciudad = ciudad
        self.id_ciente = id_ciente
        self.estado = estado
    def guardar_estudiante(self):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql= "INSERT INTO estudiantes (nombre, apellido, tipo_doc, numero_doc, correo, num_telefono, num_telefono_fijo, ciudad, estado, id_cliente) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(self.nombres, self.apellidos, self.tipo_doc, self.num_doc, self.correo, self.telefono, self.tel_fijo, self.ciudad, self.estado, self.id_ciente)
        cursor.execute(sql)
        conn.commit()
        return True
      except Exception as e:
        print(e)
        return False
      

        