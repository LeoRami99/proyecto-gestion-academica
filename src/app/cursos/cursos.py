from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .curso import Curso

cursos = Blueprint('cursos', __name__, template_folder='templates', url_prefix='/')

@cursos.route('/registro_curso')
@login_required
def index():
    return render_template('cursos.html')  

@cursos.route('/registrar_curso', methods=['POST', 'GET'])
@login_required
def registrar_curso():
    if request.method == 'POST':
        codigo_curso = request.form['codigo_curso']
        nombre_curso = request.form['nombre_curso']
        descripcion_curso = request.form['decripcion_curso']
        cantidad_hora = request.form['cantidad_hora']
        cupo_curso = request.form['cupo_curso']
        fecha_inicio = request.form['fecha_inicio']
        fecha_final = request.form['fecha_final']
        modalidad_curso = request.form['modalidad_curso']
        estado_matricula = request.form['estado_matricula']
        estado_curso = request.form['estado_curso']
        id_cliente = request.form['id_cliente']
        if codigo_curso and nombre_curso and descripcion_curso and cantidad_hora and cupo_curso and fecha_inicio and fecha_final and modalidad_curso and estado_matricula and estado_curso and id_cliente:
            curso = Curso(codigo_curso, nombre_curso, descripcion_curso, cantidad_hora, cupo_curso, fecha_inicio, fecha_final, modalidad_curso, estado_matricula, estado_curso, id_cliente)
            # curso.guardar_curso()
            if curso.guardar_curso() == True:
                flash('Curso registrado correctamente')
                return redirect(url_for('cursos.index'))
            else:
                flash('No se pudo registrar el curso')
                return redirect(url_for('cursos.index'))
        else:
            flash('No se pudo registrar el curso')
            return redirect(url_for('cursos.index'))
    else:
        return redirect(url_for('cursos.index'))

@cursos.route('/listar_cursos')
@login_required
def listar_cursos():
    curso = Curso()
    cursos = curso.obtener_cursos(current_user.id_cliente)
    # Recargar cuando se haga un cambio en la base de datos
    
    return render_template('cursos_index.html', cursos=cursos)



        


  
