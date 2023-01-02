from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from conection_mysql import obtener_conexion

inicio = Blueprint('inicio', __name__, template_folder='templates', url_prefix='/')

@inicio.route('/inicio')
@login_required
def index():
    nombre_cliente = obtener_todo_cliente(current_user.id_cliente)
    return render_template('inicio.html', nombre_cliente=nombre_cliente[2])
def obtener_todo_cliente(id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM cliente WHERE id = {0}".format(id)
    cursor.execute(sql)
    cliente = cursor.fetchone()
    return cliente