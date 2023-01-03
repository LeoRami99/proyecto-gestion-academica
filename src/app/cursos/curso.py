from conection_mysql import obtener_conexion
# Declara variables globales y constantes para la conexion
conn = obtener_conexion()
cursor = conn.cursor()
# Si la conexión no se puede hacer no dejar hacer nada
if conn is None:
    exit()
class Curso():
    def __init__(self, codigo_curso=None, nombre_curso=None, descripcion=None, cantidad_horas=None, cupo_curso=None, fecha_inicio=None, fecha_fin=None, modalidad=None, estado_matricula=None, estado=None, id_cliente=None):
        self.codigo_curso = codigo_curso
        self.nombre_curso = nombre_curso
        self.descripcion = descripcion
        self.cantidad_horas = cantidad_horas
        self.cupo_curso = cupo_curso
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.modalidad = modalidad
        self.estado_matricula = estado_matricula
        self.estado = estado
        self.id_cliente = id_cliente

    def guardar_curso(self):
        try:
            sql = """INSERT INTO curso (codigo_curso, nombre_curso, descripcion, cantidad_horas, cupo_curso, fecha_inicio, fecha_fin, modalidad, estado_matricula, estado, id_cliente) 
            VALUES ('{0}', '{1}', '{2}', {3}, {4}, '{5}', '{6}', '{7}', '{8}', '{9}', {10})""".format(self.codigo_curso, self.nombre_curso, self.descripcion, self.cantidad_horas, self.cupo_curso, self.fecha_inicio, self.fecha_fin, self.modalidad, self.estado_matricula, self.estado, self.id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def obtener_cursos(self, id_cliente):
        try:
            sql = "SELECT * FROM curso WHERE id_cliente={0}".format(id_cliente)
            cursor.execute(sql)
            cursos = cursor.fetchall()
            return cursos
        except Exception as e:
            print(e)
            return None
    # def obtener_curso(self, id_cliente):
    #     try:
    #         sql = "SELECT * FROM curso WHERE id_cliente={0}".format(id)
    #         cursor.execute(sql)
    #         curso = cursor.fetchone()
    #         return curso
    #     except Exception as e:
    #         print(e)
    #         return None
    def actualizar_curso(self, id):
        try:
            sql = """UPDATE curso SET codigo_curso='{0}', nombre_curso='{1}', descripcion='{2}', cantidad_horas={3}, cupo_curso={4}, fecha_inicio='{5}', fecha_fin='{6}', modalidad='{7}', estado_matricula='{8}', estado='{9}', id_cliente={10} WHERE id={11}""".format(self.codigo_curso, self.nombre_curso, self.descripcion, self.cantidad_horas, self.cupo_curso, self.fecha_inicio, self.fecha_fin, self.modalidad, self.estado_matricula, self.estado, self.id_cliente, id)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def eliminar_curso(self, id):
        try:
            sql = "DELETE FROM curso WHERE id={0}".format(id)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

        
       