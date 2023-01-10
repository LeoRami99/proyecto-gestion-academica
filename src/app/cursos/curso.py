from conection_mysql import obtener_conexion
# Declara variables globales y constantes para la conexion


class Curso():
    def __init__(self, nombre_curso=None, codigo_curso=None, fecha_incio=None, fecha_fin=None, horario=None, modalidad=None, duracion=None, intensidad_horaria=None, cantidad_sesiones=None, cupo_curso=None, enlace_clase=None, enlace_grabaciones=None, enlace_form_asistencia=None, estado=None, id_cliente=None):
        self.nombre_curso = nombre_curso
        self.codigo_curso = codigo_curso
        self.fecha_incio = fecha_incio
        self.fecha_fin = fecha_fin
        self.horario = horario
        self.modalidad = modalidad
        self.duracion = duracion
        self.intensidad_horaria = intensidad_horaria
        self.cantidad_sesiones = cantidad_sesiones
        self.cupo_curso = cupo_curso
        self.enlace_clase = enlace_clase
        self.enlace_grabaciones = enlace_grabaciones
        self.enlace_form_asistencia = enlace_form_asistencia
        self.estado = estado
        self.id_cliente = id_cliente
    def guardar_curso(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO curso (nombre_curso, codigo_curso, fecha_inicio, fecha_fin, horario, modalidad, duracion, intensidad_horaria, cantidad_sesiones, cupo_curso, enlace_clase, enlace_grabaciones, formulario_asistencia, estado_curso, id_cliente) 
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}')""".format(self.nombre_curso, self.codigo_curso, self.fecha_incio, self.fecha_fin, self.horario, self.modalidad, self.duracion, self.intensidad_horaria, self.cantidad_sesiones, self.cupo_curso, self.enlace_clase, self.enlace_grabaciones, self.enlace_form_asistencia, self.estado, self.id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def obtener_cursos(self, id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT * FROM curso where id_cliente = {0}".format(id_cliente)
            cursor.execute(sql)
            cursos = cursor.fetchall()
            return cursos
        except Exception as e:
            print(e)
            return False
    def obtener_curso(self, id):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT * FROM curso where id = {0}".format(id)
            cursor.execute(sql)
            curso = cursor.fetchone()
            return curso
        except Exception as e:
            print(e)
            return False
    def actualizar_curso(self, id):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """UPDATE curso SET nombre_curso = '{0}', codigo_curso = '{1}', fecha_inicio = '{2}', fecha_fin = '{3}', horario = '{4}', duracion= '{5}', intensidad_horaria = '{6}', cantidad_sesiones = '{7}', cupo_curso = '{8}', enlace_clase = '{9}', enlace_grabaciones = '{10}', formulario_asistencia = '{11}' WHERE id = {12}""".format(self.nombre_curso, self.codigo_curso, self.fecha_incio, self.fecha_fin, self.horario, self.duracion, self.intensidad_horaria, self.cantidad_sesiones, self.cupo_curso, self.enlace_clase, self.enlace_grabaciones, self.enlace_form_asistencia, id)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def eliminar_curso(self, id):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "DELETE FROM curso WHERE id = {0}".format(id)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    @classmethod
    def lista_curso_docente(self, id_curso, id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT id, id_curso, id_cliente, id_docente FROM asignacion_docente_curso WHERE id_curso = {0} AND id_cliente = {1}".format(id_curso, id_cliente)
            cursor.execute(sql)
            cursos_docente = cursor.fetchone()
            return cursos_docente
        except Exception as e:
            print(e)
            return False
    @classmethod
    def asignar_docente_curso(self, id_curso, id_docente, id_cliente, fecha_inicio, fecha_fin):
        try:
            conn= obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO asignacion_docente_curso (id_curso, id_docente, id_cliente, fecha_inicio, fecha_fin) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(id_curso, id_docente, id_cliente, fecha_inicio, fecha_fin)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
       