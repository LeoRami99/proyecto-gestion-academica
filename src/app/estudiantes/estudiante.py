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
    @classmethod
    def verificacion_estudiantes(self, num_identification, id_cliente):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql ="SELECT * FROM estudiantes WHERE numero_doc = '{0}' AND id_cliente = '{1}'".format(num_identification, id_cliente)
        cursor.execute(sql)
        conn.commit()
        if cursor.rowcount == 0:
          return False
        else:
          return True
      except Exception as e:
        print(e)
        return False
    # Se obtiene el id del estudiante y se verifica que este registrado en la base de datos
    @classmethod
    def estudiante_id(self, num_identification, id_cliente):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql ="SELECT id FROM estudiantes WHERE numero_doc = '{0}' AND id_cliente = '{1}'".format(num_identification, id_cliente)
        cursor.execute(sql)
        id_cliente = cursor.fetchone()
        conn.commit()
        if id_cliente is None:
          return False
        else:
          return id_cliente[0]
      except Exception as e:
        print(e)
        return False
    @classmethod
    def asignar_estudiante_curso(self, id_curso, id_estudiante, id_cliente, fecha_inicio, fecha_fin):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "INSERT INTO asignacion_estudiantes_curso (id_curso, id_estudiante, id_cliente, fecha_inicio, fecha_fin, activo) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(id_curso, id_estudiante, id_cliente, fecha_inicio, fecha_fin, 1)
        cursor.execute(sql)
        conn.commit()
        return True
      except Exception as e:
        print(e)
        return False
    #Contador de usuarios asignados a un curso y se hace
    @classmethod
    def count_usuarios_cupo(self, id_curso, id_cliente):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM asignacion_estudiantes_curso WHERE id_curso = '{0}' AND id_cliente = '{1}' AND activo = '{2}'".format(id_curso, id_cliente, 1)
        cursor.execute(sql)
        count = cursor.fetchone()
        conn.commit()
        return count[0]
      except Exception as e:
        print(e)
        return False

    """ 
    Se genera la información para las notas y la asistencia de cada estudiante una vez ha sido asignado 
    al curso
    """
    @classmethod
    def generar_info_asistencia(self, id_estudiante, id_curso, id_cliente):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "INSERT INTO asistencias (id_estudiante, id_curso, id_cliente) VALUES ('{0}', '{1}', '{2}')".format(id_estudiante, id_curso, id_cliente)
        cursor.execute(sql)
        conn.commit()
        return True
      except Exception as e:
        print(e)
        return False
    @classmethod
    def generar_info_calificaciones(self, id_estudiante, id_curso, id_cliente):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql="INSERT INTO calificaciones (id_estudiante, id_curso, id_cliente) VALUES ('{0}', '{1}', '{2}')".format(id_estudiante, id_curso, id_cliente)
        cursor.execute(sql)
        conn.commit()
        return True
      except Exception as e:
        print("Error en info calificaciones", e)
        return False
  
       
