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
        # retornar el id del estudiante
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

    """
    funciones para obtener la información de la asistencias y notas
    """
    @classmethod
    def obtener_asistencia_curso(self,id_curso, id_cliente):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "SELECT * FROM asistencias WHERE id_curso = '{0}' AND id_cliente = '{1}'".format(id_curso, id_cliente)
        cursor.execute(sql)
        asistencias = cursor.fetchall()
        conn.commit()
        return asistencias
      except Exception as e:
        print(e)
        return False
    @classmethod
    # Esta función trae el nombre, apellido y número de documentos del estudiate
    def obtener_estudiante(self, id_estudiante):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "SELECT nombre, apellido, numero_doc FROM estudiantes WHERE id = '{0}'".format(id_estudiante)
        cursor.execute(sql)
        estudiante = cursor.fetchone()
        conn.commit()
        return estudiante
      except Exception as e:
        print(e)
        return False
    @classmethod
    def actualizar_asistencia(self, id_estudiante, id_cliente, id_curso, asis_1, asis_2, asis_3, asis_4, asis_5, asis_6, asis_7, asis_8, asis_9, asis_10, asis_11, asis_12, asis_13, asis_14, asis_15, asis_16, asis_17, asis_18, asis_19, asis_20, asis_21, asis_22, asis_23, asis_24, asis_25, asis_26, asis_27, asis_28, asis_29, asis_30):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "UPDATE asistencias SET asis_1 = '{0}', asis_2 = '{1}', asis_3 = '{2}', asis_4 = '{3}', asis_5 = '{4}', asis_6 = '{5}', asis_7 = '{6}', asis_8 = '{7}', asis_9 = '{8}', asis_10 = '{9}', asis_11 = '{10}', asis_12 = '{11}', asis_13 = '{12}', asis_14 = '{13}', asis_15 = '{14}', asis_16 = '{15}', asis_17 = '{16}', asis_18 = '{17}', asis_19 = '{18}', asis_20 = '{19}', asis_21 = '{20}', asis_22 = '{21}', asis_23 = '{22}', asis_24 = '{23}', asis_25 = '{24}', asis_26 = '{25}', asis_27 = '{26}', asis_28 = '{27}', asis_29 = '{28}', asis_30 = '{29}' WHERE id_estudiante = '{30}' AND id_cliente = '{31}' AND id_curso = '{32}'".format(asis_1, asis_2, asis_3, asis_4, asis_5, asis_6, asis_7, asis_8, asis_9, asis_10, asis_11, asis_12, asis_13, asis_14, asis_15, asis_16, asis_17, asis_18, asis_19, asis_20, asis_21, asis_22, asis_23, asis_24, asis_25, asis_26, asis_27, asis_28, asis_29, asis_30, id_estudiante, id_cliente, id_curso)
        cursor.execute(sql)
        conn.commit()
        # ver que arroja el sql para ver si se actualiza
        print(sql)
        return True
      except Exception as e:
        print(e)
        return False
    @classmethod
    def obtener_calificaciones_curso(self, id_curso, id_cliente):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "SELECT * FROM calificaciones WHERE id_curso = '{0}' AND id_cliente = '{1}'".format(id_curso, id_cliente)
        cursor.execute(sql)
        calificaciones = cursor.fetchall()
        conn.commit()
        return calificaciones
      except Exception as e:
        print(e)
        return False
    @classmethod
    def actualizar_calificaciones(self, id_curso, id_estudiante, id_cliente, nota1, nota2, nota3, nota4, nota5, nota6, nota7, nota8, nota9, nota10, observacion):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "UPDATE calificaciones SET nota1 = '{0}', nota2 = '{1}', nota3 = '{2}', nota4 = '{3}', nota5 = '{4}', nota6 = '{5}', nota7 = '{6}', nota8 = '{7}', nota9 = '{8}', nota10 = '{9}', observacion = '{10}' WHERE id_curso = '{11}' AND id_estudiante = '{12}' AND id_cliente = '{13}'".format(nota1, nota2, nota3, nota4, nota5, nota6, nota7, nota8, nota9, nota10, observacion, id_curso, id_estudiante, id_cliente)
        cursor.execute(sql)
        conn.commit()
        return True
      except Exception as e:
        print(e)
        return False
    @classmethod
    def obtener_estudiantes(self, id_cliente):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "SELECT * FROM estudiantes WHERE id_cliente = '{0}'".format(id_cliente)
        cursor.execute(sql)
        estudiantes = cursor.fetchall()
        conn.commit()
        return estudiantes
      except Exception as e:
        print(e)
        return False
    @classmethod
    def obtener_asistencia(self, id_curso):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "SELECT estudiantes.numero_doc, estudiantes.nombre, estudiantes.apellido, asistencias.asis_1, asistencias.asis_2, asistencias.asis_3, asistencias.asis_4, asistencias.asis_5, asistencias.asis_6, asistencias.asis_7, asistencias.asis_8, asistencias.asis_9, asistencias.asis_10, asistencias.asis_11, asistencias.asis_12, asistencias.asis_13, asistencias.asis_14, asistencias.asis_15, asistencias.asis_16, asistencias.asis_17, asistencias.asis_18, asistencias.asis_19, asistencias.asis_20, asistencias.asis_21, asistencias.asis_22, asistencias.asis_23, asistencias.asis_24, asistencias.asis_25, asistencias.asis_26, asistencias.asis_27, asistencias.asis_28, asistencias.asis_29, asistencias.asis_30 FROM estudiantes INNER JOIN asistencias ON estudiantes.id = asistencias.id_estudiante AND asistencias.id_curso='{0}'".format(id_curso)
        cursor.execute(sql)
        asistencia = cursor.fetchall()
        conn.commit()
        return asistencia
      except Exception as e:
        print(e)
        return False
    @classmethod
    def obtener_calificacion(self, id_curso):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "SELECT estudiantes.numero_doc, estudiantes.nombre, estudiantes.apellido, calificaciones.nota1, calificaciones.nota2, calificaciones.nota3, calificaciones.nota4, calificaciones.nota5, calificaciones.nota6, calificaciones.nota7, calificaciones.nota8, calificaciones.nota9, calificaciones.nota10, calificaciones.observacion FROM estudiantes INNER JOIN calificaciones ON estudiantes.id = calificaciones.id_estudiante AND calificaciones.id_curso='{0}'".format(id_curso)
        cursor.execute(sql)
        calificacion = cursor.fetchall()
        conn.commit()
        return calificacion
      except Exception as e:
        print(e)
        return False