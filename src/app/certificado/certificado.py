from conection_mysql import obtener_conexion

class Certificado():
    def __init__(self, id_curso, id_cliente, id_estudiante):
        self.id_curso = id_curso
        self.id_cliente = id_cliente
        self.id_estudiante = id_estudiante

    @classmethod
    def obtener_nota(self, id_curso, id_estudiante):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """SELECT calificaciones.nota10, curso.estado_curso
            FROM calificaciones
            JOIN curso ON calificaciones.id_curso = curso.id
            WHERE calificaciones.id_estudiante = '{0}' AND calificaciones.id_curso = '{}';""".format(id_estudiante, id_curso)
            cursor.execute(sql)
            nota = cursor.fetchone()
            conn.close()
            return nota
        except Exception as e:
            print(e)
            return None
    @classmethod
    def obtener_asistencia(self, id_curso, id_estudiante):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """SELECT SUM(asistencias.asis_1 + asistencias.asis_2 + asistencias.asis_3 + asistencias.asis_4 + asistencias.asis_5 + asistencias.asis_6 + asistencias.asis_7 + asistencias.asis_8 + asistencias.asis_9 + asistencias.asis_10 + asistencias.asis_11 + asistencias.asis_12 + asistencias.asis_13 + asistencias.asis_14 + asistencias.asis_15 + asistencias.asis_16 + asistencias.asis_17 + asistencias.asis_18 + asistencias.asis_19 + asistencias.asis_20 + asistencias.asis_21 + asistencias.asis_22 + asistencias.asis_23 + asistencias.asis_24 + asistencias.asis_25 + asistencias.asis_26 + asistencias.asis_27 + asistencias.asis_28 + asistencias.asis_29 + asistencias.asis_30) as asistencia_final FROM asistencias WHERE id_curso='{0}' and id_estudiante='{1}';""".format(id_curso, id_estudiante)
            cursor.execute(sql)
            asistencia = cursor.fetchone()
            conn.close()
            return asistencia
        except Exception as e:
            print(e)
            return None
    @classmethod
    def obtener_info_curso(self, codigo_curso):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql= """SELECT curso.id, curso.nombre_curso, curso.codigo_curso, curso.duracion, curso.id_cliente FROM curso WHERE codigo_curso='{0}'""".format(codigo_curso)
        cursor.execute(sql)
        info_curso = cursor.fetchone()
        conn.close()
        return info_curso
      except Exception as e:
        print(e)
        return None
    @classmethod
    def obtener_info_curso_maestro(self, id_curso):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql= """SELECT reg_cursos.max_asistencia FROM reg_cursos WHERE id='{0}'""".format(id_curso)
        cursor.execute(sql)
        info_curso = cursor.fetchone()
        conn.close()
        return info_curso
      except Exception as e:
        print(e)
        return None

    @classmethod
    def obtener_info_estudiante(self, num_doc, id_cliente):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql= """SELECT estudiante.id, estudiante.nombre, estudiante.apellido, estudiante.num_doc FROM estudiante WHERE num_doc='{0}' and id_cliente='{1}'""".format(num_doc, id_cliente)
        cursor.execute(sql)
        info_estudiante = cursor.fetchone()
        conn.close()
        return info_estudiante
      except Exception as e:
        print(e)
        return None


  

    


