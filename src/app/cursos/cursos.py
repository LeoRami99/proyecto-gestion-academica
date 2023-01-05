from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .curso import Curso

cursos = Blueprint('cursos', __name__, template_folder='templates', url_prefix='/')

@cursos.route('/registro_curso')
@login_required
def index():
    if current_user.rol == 'AD':
        return render_template('cursos.html')
    else:
        return redirect(url_for('inicio.index'))

@cursos.route('/registrar_curso', methods=['POST', 'GET'])
@login_required
def registrar_curso():
    if request.method == 'POST':
        nombre_curso= request.form['nombre_curso']
        codigo_curso = request.form['codigo_curso']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_final']
        horario = request.form['horario_curso']
        modalidad_curso = request.form['modalidad_curso']
        duracion_curso = request.form['duracion_curso']
        intensidad_horaria = request.form['intensidad_horaria']
        cantidad_sesion = request.form['cantidad_sesiones']
        cupo_curso = request.form['cupo_curso']
        enlace_clase = request.form['enlace_clase']
        enlace_grabaciones = request.form['enlace_grabaciones']
        enlace_form_asistencia = request.form['enlace_form_asistencia']
        estado_curso = request.form['estado_curso']
        id_cliente = request.form['id_cliente']
        print(nombre_curso, codigo_curso, fecha_inicio, fecha_fin, horario, modalidad_curso, duracion_curso, intensidad_horaria, cantidad_sesion, cupo_curso, enlace_clase, enlace_grabaciones, enlace_form_asistencia, estado_curso, id_cliente) 
        if nombre_curso and codigo_curso and fecha_inicio and fecha_fin and horario and modalidad_curso and duracion_curso and intensidad_horaria and cantidad_sesion and cupo_curso and enlace_clase and enlace_grabaciones and enlace_form_asistencia and estado_curso and id_cliente:
            curso = Curso(nombre_curso, codigo_curso, fecha_inicio, fecha_fin, horario, modalidad_curso, duracion_curso, intensidad_horaria, cantidad_sesion, cupo_curso, enlace_clase, enlace_grabaciones, enlace_form_asistencia, estado_curso, id_cliente)
            if curso.guardar_curso():
                flash('Curso registrado correctamente')
                return redirect(url_for('cursos.listar_cursos'))
            else:
                flash('Error al registrar curso')
                return redirect(url_for('cursos.index'))
        else:
            flash('Por favor, complete los campos')
            return redirect(url_for('cursos.index'))
    else:
        flash('Error al registrar curso')
        return redirect(url_for('cursos.index'))
        

@cursos.route('/listar_cursos')
@login_required
def listar_cursos():
    curso = Curso()
    cursos = curso.obtener_cursos(current_user.id_cliente)
    
    return render_template('cursos_index.html', cursos=cursos)



        


  
