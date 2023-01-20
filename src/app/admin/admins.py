import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.clientes.cliente import Cliente
from app.admin.admin import Admin

admin = Blueprint('admin', __name__,
                  template_folder='templates', url_prefix='/admin')


@admin.route('/')
def index():
    clientes = Cliente.obtener_clientes()
    if clientes is False:
        flash('No se pudo obtener los clientes')
        return redirect(url_for('admin.index'))
    else:
        return render_template('admin.html', clientes=clientes)


@admin.route('/registrar_administrador', methods=['POST'])
def registrar_administrador():
    expresiones_regulares = {
        'username': r'^[a-zA-Z0-9_-]{4,16}$',
        'contrasena': r'^[a-zA-Z0-9_-]{6,18}$',
        'nombre': r'^[a-zA-Z]{2,50}$',
        'apellido': r'^[a-zA-Z]{2,50}$',
        'correo': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'telefono': r'^[0-9]{7,10}$',
        'cliente': r'^[0-9]{1,10}$',
        'rol': r'^[0-9]{1,10}$'
    }

    try:
        if request.method == 'POST':
            nombre_usuario = request.form['username']
            contrasena = request.form['contrasena']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['correo']
            telefono = request.form['telefono']
            cliente = request.form['cliente']
            rol = request.form['rol']
            if nombre_usuario and len(contrasena)>=6 and contrasena and nombre and apellido and email and telefono and cliente and rol:
                # verficar que los datos esten y no tenga expresiones regulares antes de registrar
                if not re.match(expresiones_regulares['username'], nombre_usuario) and not re.match(expresiones_regulares['contrasena'], contrasena) and not re.match(expresiones_regulares['nombre'], nombre) and not re.match(expresiones_regulares['apellido'], apellido) and not re.match(expresiones_regulares['correo'], email) and not re.match(expresiones_regulares['telefono'], telefono) and not re.match(expresiones_regulares['cliente'], cliente) and not re.match(expresiones_regulares['rol'], rol):
                    flash('Los datos no son validos')
                    return redirect(url_for('admin.index'))
                else:
                    # verificar que el nombre de usuario no exista
                    existe = Admin.obtener_usernames(nombre_usuario)
                    if existe:
                        flash('Este nombre de usuario ya existe')
                        return redirect(url_for('admin.index'))
                    else:
                        admin = Admin(nombre_usuario, contrasena, nombre.title(), apellido.title(), email, telefono, rol, cliente)
                        
                        if admin.registrar_administrador():
                            flash('Administrador registrado correctamente')
                            return redirect(url_for('admin.index'))
                        else:
                            flash('No se pudo registrar el administrador')
                            return redirect(url_for('admin.index'))
            else:
                flash('Los datos no son validos')
                return redirect(url_for('admin.index'))
        else:
            flash('No se pudo registrar el administrador')
            return redirect(url_for('admin.index'))
    except Exception as e:
        print(e)
        flash('No se pudo registrar el administrador')
        return redirect(url_for('admin.index'))

# Metodo para obtener los nombres de usuarios mediante ajax api rest
@admin.route('/api/obtener_nombres_usuarios', methods=['POST'])
def obtener_nombres_usuarios():
    if request.method == 'POST':
        nombre_usuario = request.form['username']
        if nombre_usuario:
            existe = Admin.obtener_usernames(nombre_usuario)
            if existe:
                return 'Este nombre de usuario ya existe'
            else:
                return 'Este nombre de usuario esta disponible'
        else:
            return 'Este campo no puede estar vacio'
    else:
        return 'No se pudo obtener el nombre de usuario'
