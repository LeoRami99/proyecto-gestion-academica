from conection_mysql import obtener_conexion

class Docente():
    def __init__(self, nombre_usuario=None, nombres=None, apellidos=None, correo=None, password=None, numero_cel=None, numero_tel_fijo=None, rol=None, estado=None, tipo_doc=None, num_doc=None, profesion=None, id_cliente=None):
        self.nombre_usuario = nombre_usuario
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.password = password
        self.numero_cel = numero_cel
        self.numero_tel_fijo = numero_tel_fijo
        self.rol = rol
        self.estado = estado
        self.tipo_doc = tipo_doc
        self.num_doc = num_doc
        self.profesion = profesion
        self.id_cliente = id_cliente
    
    def guardar_docente(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql="""INSERT INTO usuarios (nombre_usuario, nombre, apellido, correo, password, telefono, tel_fijo, rol, estado, tipo_doc, numero_doc, profesion, id_cliente) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}')""".format(self.nombre_usuario, self.nombres, self.apellidos, self.correo, self.password, self.numero_cel, self.numero_tel_fijo, self.rol, self.estado, self.tipo_doc, self.num_doc, self.profesion, self.id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    @classmethod
    def obtenerDocentesCliente(self , id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql="""SELECT id, nombre_usuario, nombre, apellido, correo, telefono, tel_fijo, estado, tipo_doc, numero_doc, profesion, id_cliente FROM usuarios WHERE id_cliente={0} AND rol='DOC'""".format(id_cliente)
            cursor.execute(sql)
            filas = cursor.fetchall()
            return filas
        except Exception as e:
            print(e)
            return False
    @classmethod
    def obtenerDocente(self, id):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql="""SELECT id, nombre_usuario, nombre, apellido, correo, telefono, tel_fijo, estado, tipo_doc, numero_doc, profesion, id_cliente FROM usuarios WHERE id={0}""".format(id)
            cursor.execute(sql)
            fila = cursor.fetchone()
            return fila
        except Exception as e:
            print(e)
            return False
    def actualizarDocente(self, id, id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql="""UPDATE usuarios SET nombre='{0}', apellido='{1}', correo='{2}', telefono='{3}', tel_fijo='{4}', estado='{5}', numero_doc='{6}', profesion='{7}' WHERE id={8} AND id_cliente={9}""".format(self.nombres, self.apellidos, self.correo, self.numero_cel, self.numero_tel_fijo, self.estado, self.num_doc, self.profesion, id, id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    @classmethod
    def eliminarDocente(self, id, id_cliente):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql="""DELETE FROM usuarios WHERE id={0} AND id_cliente={1}""".format(id, id_cliente)
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    

        

    
         