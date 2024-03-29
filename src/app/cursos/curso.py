from conection_mysql import obtener_conexion
# Declara variables globales y constantes para la conexion


class Curso():
    def __init__(self, nombre_curso=None, codigo_curso=None, fecha_incio=None, fecha_fin=None, horario=None, modalidad=None, duracion=None, intensidad_horaria=None, cantidad_sesiones=None, cupo_curso=None, enlace_clase=None, enlace_grabaciones=None, enlace_form_asistencia=None, estado=None, id_cliente=None, ubicacion=None, id_reg_curso=None):
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
        self.ubicacion = ubicacion
        self.id_reg_curso = id_reg_curso

    def guardar_curso(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO curso (nombre_curso, codigo_curso, fecha_inicio, fecha_fin, horario, modalidad, duracion, intensidad_horaria, cantidad_sesiones, cupo_curso, enlace_clase, enlace_grabaciones, formulario_asistencia, estado_curso, id_cliente, lugar_presencial, id_reg_cursos) 
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}')""".format( self.nombre_curso, self.codigo_curso, self.fecha_incio, self.fecha_fin, self.horario, self.modalidad, self.duracion, self.intensidad_horaria, self.cantidad_sesiones, self.cupo_curso, self.enlace_clase, self.enlace_grabaciones, self.enlace_form_asistencia, self.estado, self.id_cliente, self.ubicacion, self.id_reg_curso)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print("error al guarda:", e)
            return False

    def obtener_cursos(self, id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT * FROM curso where id_cliente = {0}".format(
                id_cliente)
            cursor.execute(sql)
            cursos = cursor.fetchall()
            return cursos
        except Exception as e:
            print(e)
            return False
    # reigstro y consulta de cursos maestros
    def obtener_reg_curso(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT * FROM reg_cursos"
            cursor.execute(sql)
            cursos = cursor.fetchall()
            if cursos is None:
                return False
            else:
                return cursos
        except Exception as e:
            print(e)
            return False
    @classmethod
    def obtener_reg_curso_id(self, id):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT * FROM reg_cursos WHERE id='{0}'".format(id)
            cursor.execute(sql)
            cursos = cursor.fetchone()
            if cursos is None:
                return False
            else:
                return cursos
        except Exception as e:
            print(e)
            return False
    @classmethod
    def guardar_curso_master(self, nombre_curso, duracion_curso, cupo_curso, cantidad_notas, cantidad_asistencias, cantidad_asis_aprobar, id_cliente ):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO reg_cursos (nombre_curso, duracion_curso, cupo_curso, cantidad_notas, cantidad_asistencias, max_asistencia, id_cliente) 
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(nombre_curso, duracion_curso, cupo_curso, cantidad_notas, cantidad_asistencias, cantidad_asis_aprobar, id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    @classmethod
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
            sql = """UPDATE curso SET nombre_curso = '{0}', codigo_curso = '{1}', fecha_inicio = '{2}', fecha_fin = '{3}', horario = '{4}', duracion= '{5}', intensidad_horaria = '{6}', cantidad_sesiones = '{7}', cupo_curso = '{8}', enlace_clase = '{9}', enlace_grabaciones = '{10}', formulario_asistencia = '{11}' , lugar_presencial = '{12}' WHERE id = {13}""".format(
                self.nombre_curso, self.codigo_curso, self.fecha_incio, self.fecha_fin, self.horario, self.duracion, self.intensidad_horaria, self.cantidad_sesiones, self.cupo_curso, self.enlace_clase, self.enlace_grabaciones, self.enlace_form_asistencia, self.ubicacion, id)
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
            sql = "SELECT id, id_curso, id_cliente, id_docente FROM asignacion_docente_curso WHERE id_curso = {0} AND id_cliente = {1}".format(
                id_curso, id_cliente)
            cursor.execute(sql)
            cursos_docente = cursor.fetchone()
            return cursos_docente
        except Exception as e:
            print(e)
            return False

    @classmethod
    def asignar_docente_curso(self, id_curso, id_docente, id_cliente, fecha_inicio, fecha_fin):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO asignacion_docente_curso (id_curso, id_docente, id_cliente, fecha_inicio, fecha_fin) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(
                id_curso, id_docente, id_cliente, fecha_inicio, fecha_fin)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def obtener_cursos_docente(self, id_docente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """SELECT * FROM asignacion_docente_curso WHERE id_docente={0}""".format(
                id_docente)
            cursor.execute(sql)
            filas = cursor.fetchall()
            return filas
        except Exception as e:
            return False

    # funcion para obtener el id del ultimo curso para generar el codigo

    @classmethod
    def obtener_id_curso(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT MAX(id) FROM curso"
            cursor.execute(sql)
            id_curso = cursor.fetchone()

            if id_curso[0] is None:
                return 0
            else:
                return id_curso[0]
        except Exception as e:
            print(e)
            return False

    @classmethod
    def obtener_curso_id(self, codigo_curso):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = "SELECT id FROM curso WHERE codigo_curso = '{0}'".format(
                codigo_curso)
            cursor.execute(sql)
            id_curso = cursor.fetchone()
            if id_curso != None:
                return id_curso[0]
            else:
                return False
        except Exception as e:
            print(e)
            return False

    """
        Estas funciones son para cumplir el rol de parametros para cerrar el curso.
    """

    @classmethod
    def consulta_notas_curso(self, id_curso):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """SELECT asignacion_estudiantes_curso.id_estudiante, (calificaciones.nota1 + calificaciones.nota2 + calificaciones.nota3 + calificaciones.nota4 + calificaciones.nota5+ calificaciones.nota6 + calificaciones.nota7 + calificaciones.nota8 + calificaciones.nota9) as nota
                FROM asignacion_estudiantes_curso 
                INNER JOIN calificaciones ON asignacion_estudiantes_curso.id_estudiante = calificaciones.id_estudiante 
                AND asignacion_estudiantes_curso.id_curso = calificaciones.id_curso 
                WHERE asignacion_estudiantes_curso.id_curso={0}""".format(id_curso)
            cursor.execute(sql)
            filas = cursor.fetchall()   
            return filas
        except Exception as e:
            print(e)
            return False

    @classmethod
    def asistencia_estudiante_curso(self, id_estudiante, id_curso):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """SELECT SUM(asis_1 + asis_2 + asis_3+ asis_4+ asis_5+ asis_6+ asis_7+asis_8+asis_9+asis_10+asis_11 + asis_12 + asis_13+ asis_14+ asis_15+ asis_16+ asis_17+asis_18+asis_19+asis_20+asis_21 + asis_22 + asis_23+ asis_24+ asis_25+asis_26+asis_27+asis_28+asis_29+asis_30) as asistencias FROM asistencias WHERE id_estudiante = '{0}' AND id_curso = '{1}'""".format(
                id_estudiante, id_curso)
            cursor.execute(sql)
            filas = cursor.fetchone()
            return filas[0]
        except Exception as e:
            print(e)
            return False
    # Contador de estudiantes por curso

    @classmethod
    def count_estudiantes_curso(self, id_curso, id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """SELECT COUNT(*) FROM asignacion_estudiantes_curso WHERE id_curso = {0} AND id_cliente = {1}""".format(
                id_curso, id_cliente)
            cursor.execute(sql)
            filas = cursor.fetchone()
            return filas[0]
        except Exception as e:
            print(e)
            return False

    @classmethod
    def estado_curso(self, id_curso, id_cliente):
        try:

            cantidad_estudiantes = self.count_estudiantes_curso(id_curso, id_cliente)
            notas_estudiantes = self.consulta_notas_curso(id_curso)
            lista_notas_finales = []
            lista_asistencia_estudiante = []
            lista_result_condiciones = []
            # se obtiene los datos necesarios para las calificaciones y notas
            id_reg_curso=self.obtener_curso(id_curso)[17]
            infomacion_reg_curso = self.obtener_reg_curso_id(id_reg_curso)
            max_asistencias = infomacion_reg_curso[6]
            max_notas = infomacion_reg_curso[4]
            
            # información de los porcentajes de cierre del curso
            
            for indice in notas_estudiantes:
                # colocar el id y la asistencia
                lista_asistencia_estudiante.append([indice[0], self.asistencia_estudiante_curso(indice[0], id_curso)])
            


            for indice in notas_estudiantes:
                # colocar el id y la nota final
                print("este es el maximo de notas", indice[1]/max_notas)
                lista_notas_finales.append(
                    [indice[0], round(indice[1]/max_notas, 2)])
            

            for indice in zip(lista_notas_finales, lista_asistencia_estudiante):
                print("Esta son las notas de los estudiantes:", indice)
                if indice[0][1] >= 3.0 and indice[1][1] >= max_asistencias:
                    lista_result_condiciones.append([indice[0][0], True])
                elif indice[0][1] < 3.0 and indice[1][1] >= max_asistencias:
                    lista_result_condiciones.append([indice[0][0], False])
                elif indice[0][1] >= 3.0 and indice[1][1] < max_asistencias:
                    lista_result_condiciones.append([indice[0][0], False])
                elif indice[0][1] < 3.0 and indice[1][1] < max_asistencias:
                    lista_result_condiciones.append([indice[0][0], True])
            # se hace que cuando todos esten en verdadero retornar verdadero para confirmar el cambio del curso
            contador = 0
            for indice in lista_result_condiciones:
                if indice[1] == True:
                    contador += 1
                print("Este es el contador:", contador)
            if contador == cantidad_estudiantes and cantidad_estudiantes > 0:
                return True
            else:
                return False

        except Exception as e:
            print(e)
            return False

    """ 
    funciones para la asignación del cierre del curso cuando se registre
    el curso
    
    """

    @classmethod
    def asignar_cierre_curso(self, id_curso, id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO cierre_cursos (id_curso, id_cliente) VALUES ('{0}', '{1}')""".format(id_curso, id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def cerrar_curso(self, id_curso, id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """UPDATE curso SET estado_curso = 0 WHERE id = '{0}' AND id_cliente = {1}""".format(id_curso, id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print("Aqui es el erro:", e)
            return False
    @classmethod
    def fecha_cerrar_curso(self, id_curso, id_cliente, fecha_cierre):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql="""UPDATE cierre_cursos SET fecha_cierre = '{0}' WHERE id_curso = '{1}' AND id_cliente = {2}""".format(fecha_cierre, id_curso, id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    """ Fin funciones de cierre de curso """



    @classmethod
    def reactivar_curso(sefl, id_curso, id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """UPDATE curso SET estado_curso = 1 WHERE id = '{0}' AND id_cliente = {1}""".format(
                id_curso, id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # Se obtiene toda la información del curso concatenado con el nombre del docente asignado
    @classmethod
    def obtener_curso_docente(self, id_curso):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """SELECT usuarios.nombre as 'Nombre del Docente', usuarios.apellido as 'Apellidos del Docente', curso.* FROM asignacion_docente_curso
                JOIN curso ON asignacion_docente_curso.id_curso = curso.id
                JOIN usuarios ON asignacion_docente_curso.id_docente = usuarios.id
                WHERE asignacion_docente_curso.id_curso = {0}""".format(id_curso)
            cursor.execute(sql)
            filas = cursor.fetchone()
            if cursor.rowcount == 0:
                return None
            else:
                return filas
        except Exception as e:
            print("prueba de error", e)
            return False
    """ solo se obtiene el estado del curso al que se le pasa el id """
    @classmethod
    def obtener_estado_curso(self, id_curso):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """SELECT estado_curso FROM curso WHERE id = {0}""".format(id_curso)
            cursor.execute(sql)
            filas = cursor.fetchone()
            if cursor.rowcount == 0:
                return 0
            else:
                return filas[0]
        except Exception as e:
            print("prueba de error", e)
            return False
    # Traer la calificaciones y las asistencias de los estudiantes asignados de los estudiantes para enviar un correo.
    @classmethod
    def calificacion_final(self, id_curso):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """SELECT estudiantes.id, estudiantes.nombre, estudiantes.apellido , estudiantes.correo, calificaciones.nota10 FROM calificaciones JOIN estudiantes ON calificaciones.id_estudiante = estudiantes.id WHERE calificaciones.id_curso={0}""".format(id_curso)
            cursor.execute(sql)
            filas = cursor.fetchone()
            if cursor.rowcount == 0:
                return None
            else:
                return filas[0]
        except Exception as e:
            print("prueba de error", e)
            return False
    # @classmethod
    # # def asistencia_final(self, id_curso)
    # #     try:
    # #         conn = obtener_conexion()
    # #         cursor = conn.cursor()
            
    # #         cursor.execute(sql)
    # #         filas = cursor.fetchone()
    # #         if cursor.rowcount == 0:
    # #             return None
    # #         else:
    # #             return filas[0]