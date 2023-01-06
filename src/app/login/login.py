from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
# Clase usuario
from .logueo import Usuario
# Conexión a la base de datos
from conection_mysql import obtener_conexion

# blueprint de login
login_page = Blueprint('login_page', __name__, template_folder='templates', url_prefix='/')
conn = obtener_conexion()


@login_page.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inicio.index'))
    else:
        return render_template('login.html')
@login_page.route('/login_sistema', methods=['POST'])
def login_sistem():
    try:
        if request.method == 'POST':
            nombre_usuario = request.form['usuario']
            contrasena = request.form['password']
            if nombre_usuario and contrasena:
                consulta= Usuario.id_nombreuser(nombre_usuario)
                
                # print('consulta', consulta)
                user = Usuario(consulta, nombre_usuario, contrasena)
                usuario = user.login(conn)
                if usuario != None:
                    if usuario.contrasena is True:
                        login_user(usuario)
                        return redirect(url_for('inicio.index'))
                    else:
                        flash('Usuario o contraseña incorrectos')
                        return redirect(url_for('login_page.login'))
                else:
                    flash('Usuario o contraseña incorrectos')
                    return redirect(url_for('login_page.login'))
                
            else:
                flash('Por favor, complete los campos')
                return redirect(url_for('login_page.login'))
        else:
            flash('Por favor, complete los campos')
            return redirect(url_for('login_page.login'))
    except Exception as e:
        flash('Error al iniciar sesión')
        return redirect(url_for('login_page.login'))


@login_page.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page.login'))
