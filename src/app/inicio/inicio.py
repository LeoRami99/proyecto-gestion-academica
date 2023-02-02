from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from conection_mysql import obtener_conexion
from app.inicio.stats import Stats

from app.clientes.cliente import Cliente
cliente_info=Cliente()


inicio = Blueprint('inicio', __name__, template_folder='templates', url_prefix='/')

@inicio.route('/inicio')
@login_required
def index():
    conteo_estudiantes = Stats().conteo_estudiantes(current_user.id_cliente)
    conteo_curso = Stats().conteo_cursos(current_user.id_cliente)
    conteo_cursos_finalizados = Stats().conteo_cursos_finalizados(current_user.id_cliente)
    conteo_docentes = Stats().conteo_docentes(current_user.id_cliente)
    cliente=cliente_info.obtener_cliente(current_user.id_cliente)
    nombre_cliente = obtener_todo_cliente(current_user.id_cliente)
    return render_template('inicio.html', nombre_cliente=nombre_cliente[2], conteo_estudiantes=conteo_estudiantes, conteo_curso=conteo_curso,conteo_cursos_finalizados=conteo_cursos_finalizados, conteo_docentes=conteo_docentes,cliente=cliente)
def obtener_todo_cliente(id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "SELECT * FROM cliente WHERE id = {0}".format(id)
        cursor.execute(sql)
        cliente = cursor.fetchone()
        return cliente
    except Exception as e:
        print('Error al obtener cliente', e)
        return None
@inicio.route('/')
# @login_required
def inicio_page():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('inicio.index'))
        else:
            return redirect(url_for('login_page.login'))
    except Exception as e:
        print('Error al redirigir al inicio', e)
        return redirect(url_for('login_page.login'))
