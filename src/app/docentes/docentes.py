from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .docente import Docente
from werkzeug.security import generate_password_hash





docentes = Blueprint('docentes', __name__, template_folder='templates', url_prefix='/')
# Habilirar cors para que se pueda hacer la consulta ajax
# from flask_cors import CORS
# CORS(docentes)

# ruta donde se registra los docentes
@docentes.route('/docentes-registro')
@login_required
def registroDocentes():
    if current_user.rol == 'AD':
        return render_template('docentes_registro.html')
    else:
        return redirect(url_for('inicio.index'))
    

@docentes.route('/docentes/registrar', methods=['POST'])
@login_required
def registrar():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        password = request.form['password']
        numero_cel = request.form['numero_cel']
        numero_tel_fijo = request.form['numero_tel_fijo']
        rol = request.form['rol']
        estado = request.form['estado']
        tipo_doc = request.form['tipo_doc']
        num_doc = request.form['num_doc']
        profesion = request.form['profesion']
        id_cliente = request.form['id_cliente']
        if nombre_usuario and nombres and apellidos and correo and password and numero_cel and numero_tel_fijo and rol and estado and tipo_doc and num_doc and profesion and id_cliente:
            docente = Docente(nombre_usuario, nombres, apellidos, correo, generate_password_hash(password), numero_cel, numero_tel_fijo, rol, estado, tipo_doc, num_doc, profesion, id_cliente)
            if docente.guardar_docente():
                flash('Docente registrado correctamente')
                return redirect(url_for('docentes.index'))
            else:
                flash('Error al registrar docente')
                return redirect(url_for('docentes.index'))
        else:
            flash('Por favor complete todos los campos')
            return redirect(url_for('docentes.index'))
    else:
        return redirect(url_for('docentes.index'))

# ruta donde se edita los docentes
@docentes.route('/docentes/editar', methods=['POST'])
@login_required
def editar():
    if request.method == 'POST':
        id_usuario = request.form['id_docente']
        numero_documento = request.form['numero_documento']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        telefono_fijo = request.form['telefono_fijo']
        estado = request.form['estado']
        profesion = request.form['profesion']
        if id_usuario and numero_documento and nombre and apellido and correo and telefono and telefono_fijo and estado and profesion:  
            docente = Docente(num_doc=numero_documento, nombres=nombre, apellidos=apellido, correo=correo, numero_cel=telefono, numero_tel_fijo=telefono_fijo, estado=estado, profesion=profesion)
            if docente.actualizarDocente(id_usuario, current_user.id_cliente):
                flash('Docente editado correctamente')
                return redirect(url_for('docentes.index'))
            else:
                flash('Error al editar docente')
                return redirect(url_for('docentes.index'))
        else:
            flash('Por favor complete todos los campos')
            return redirect(url_for('docentes.index'))
    else:
        return redirect(url_for('docentes.index'))


# ruta donde se elimina los docentes
@docentes.route('/docentes/eliminar/<int:id_docente>' , methods=['GET'])
@login_required
def eliminar(id_docente):
    if request.method == 'GET':
        docente = Docente()
        if docente.eliminarDocente(id_docente, current_user.id_cliente):
            flash('Docente eliminado correctamente')
            return redirect(url_for('docentes.index'))
        else:
            flash('Error al eliminar docente')
            return redirect(url_for('docentes.index'))
    else:
        return redirect(url_for('docentes.index'))

# ruta donde se listan los docentes por cliente
@docentes.route('/docentes')
@login_required
def index():
    docentes = Docente.obtenerDocentesCliente(current_user.id_cliente)
    return render_template('docentes_lista.html', docentes=docentes)



##########################################################################
# --------------------- Rutas para la consulta ajax -------------------- #
##########################################################################

# Hacer ruta para consulta ajax si existe el nombre de usuario en la base de datos
@docentes.route('/docentes/consultar_usuario', methods=['POST'])
@login_required
def consultar_usuario():
    from conection_mysql import obtener_conexion
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            if request.method == 'POST':
                nombre_usuario = request.form['nombre_usuario']
                
                cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = '{0}'".format(nombre_usuario))
                data = cursor.fetchall()
        # Devolver el datos adecuado para la consulta ajax
                if len(data) > 0:
                    return 'Este nombre de usuario ya existe'
                else:
                    return 'Este nombre de usuario esta disponible'
            else:
                return "Error en la consulta"
        

# ruta donde donde trae los datos del docente para editar /docentes/datos/modal con ajax
@docentes.route('/docentes/datos/modal', methods=['POST'])
@login_required
def datos_modal():
    if request.method == 'POST':
        id_usuario = request.form['id_docente']
        docente = Docente.obtenerDocente(id_usuario)
        # arreglar objeto para que se pueda enviar a ajax request
        docente = {
            'id_usuario': docente[0],
            'nombre_usuario': docente[1],
            'nombres': docente[2],
            'apellidos': docente[3],
            'correo': docente[4],
            'numero_cel': docente[5],
            'numero_tel_fijo': docente[6],
            'estado': docente[7],
            'tipo_doc': docente[8],
            'num_doc': docente[9],
            'profesion': docente[10],
            'id_cliente': docente[11]
        }
        return docente
    else:
        return 'Error'
        
        




