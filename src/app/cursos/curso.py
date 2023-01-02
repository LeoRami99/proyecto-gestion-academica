from conection_mysql import Connection

class Curso():
    def __init__(self, id, nombre, descripcion, id_cliente, id_usuario, estado):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_cliente = id_cliente
        self.id_usuario = id_usuario
        self.estado = estado
    def guardar(self):
        conn = Connection()
        cursor = conn.cursor()
        sql = "INSERT INTO curso (nombre, descripcion, id_cliente, id_usuario, estado) VALUES ('{0}', '{1}', {2}, {3}, {4})".format(self.nombre, self.descripcion, self.id_cliente, self.id_usuario, self.estado)
        cursor.execute(sql)
        conn.commit()
        conn.close()
    @classmethod
    def obtener_cursos(self, id_cliente):
        conn = Connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM curso WHERE id_cliente = {0}".format(id_cliente)
        cursor.execute(sql)
        cursos = cursor.fetchall()
        conn.close()
        return cursos
    @classmethod
    def obtener_curso(self, id):
        conn = Connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM curso WHERE id = {0}".format(id)
        cursor.execute(sql)
        curso = cursor.fetchone()
        conn.close()
        return curso
    def actualizar(self):
        conn = Connection()
        cursor = conn.cursor()
        sql = "UPDATE curso SET nombre = '{0}', descripcion = '{1}', id_cliente = {2}, id_usuario = {3}, estado = {4} WHERE id = {5}".format(self.nombre, self.descripcion, self.id_cliente, self.id_usuario, self.estado, self.id)
        cursor.execute(sql)
        conn.commit()
        conn.close()
    def eliminar(self):
        conn = Connection()
        cursor = conn.cursor()
        sql = "DELETE FROM curso WHERE id = {0}".format(self.id)
        cursor.execute(sql)
        conn.commit()
        conn.close()