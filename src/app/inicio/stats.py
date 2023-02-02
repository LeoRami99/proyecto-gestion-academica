from conection_mysql import obtener_conexion
class Stats():
  def __init__(self) -> None:
    pass
  def conteo_estudiantes(self, id_cliente):
    try:
      conn = obtener_conexion()
      cursor  = conn.cursor()
      sql = "SELECT COUNT(*) FROM estudiantes WHERE id_cliente = '{0}'".format(id_cliente)
      cursor.execute(sql)
      conteo = cursor.fetchone()
      return conteo[0]
    except Exception as e:
      print(e)
      return None
  def conteo_cursos(self, id_cliente):
    try:
      conn = obtener_conexion()
      cursor  = conn.cursor()
      sql = "SELECT COUNT(*) FROM curso WHERE id_cliente = '{0}' AND estado_curso=1".format(id_cliente)
      cursor.execute(sql)
      conteo = cursor.fetchone()
      return conteo[0]
    except Exception as e:
      print(e)
      return None
  def conteo_cursos_finalizados(self, id_cliente):
    try:
      conn = obtener_conexion()
      cursor  = conn.cursor()
      sql = "SELECT COUNT(*) FROM curso WHERE id_cliente = '{0}' AND estado_curso=0".format(id_cliente)
      cursor.execute(sql)
      conteo = cursor.fetchone()
      return conteo[0]
    except Exception as e:
      print(e)
      return None
  def conteo_docentes(self, id_cliente):
    try:
      conn = obtener_conexion()
      cursor  = conn.cursor()
      sql ="SELECT COUNT(*) FROM `usuarios` WHERE rol='DOC' and id_cliente='{0}' AND estado=1".format(id_cliente)
      cursor.execute(sql)
      conteo = cursor.fetchone()
      return conteo[0]
    except Exception as e:
      print(e)
      return None
