import io
from os import sendfile
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, Response, send_file
from flask_login import login_required, current_user
from .curso import Curso
from app.docentes.docente import Docente
from app.estudiantes.estudiante import Estudiante
from openpyxl import Workbook
import xlsxwriter

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
    if current_user.rol == 'AD':
        curso = Curso()
        cursos = curso.obtener_cursos(current_user.id_cliente)
        # Datos del docente
        docente = Docente()
        docentes = docente.obtenerDocentesCliente(current_user.id_cliente)
        # Condición para verificar si se asigno el docente al curso
        lista_cursos = []
        for curso_lista in cursos:
            if curso.lista_curso_docente(curso_lista[0], current_user.id_cliente) != None:
                # Se agrega el curso + el nombre del docente
                cursoxdocente = docente.obtenerDocente(curso.lista_curso_docente(curso_lista[0], current_user.id_cliente)[3])
                docente_nombre_apellido = cursoxdocente[2] + ' ' + cursoxdocente[3] 
                lista_cursos.append(curso_lista + (docente_nombre_apellido,))
            else:
                # Se agrega el curso + sin asignar
                lista_cursos.append(curso_lista + ('Sin asignar',))
        return render_template('cursos_index.html', cursos=lista_cursos, docentes=docentes)
    elif current_user.rol == 'DOC':
        #Solo listar los cursos que se le fueron asignados a el docente
        curso = Curso()
        asig_doc = curso.obtener_cursos_docente(current_user.id)
        cursos = curso.obtener_cursos(current_user.id_cliente)
        listar_cursos = []
        for cursos in zip(cursos, asig_doc):
            if cursos[1] != None:
                listar_cursos.append(cursos[0])
            else:
                pass
        return render_template('cursos_index.html', cursos=listar_cursos)
    else:
        flash('No tiene permisos para acceder a esta sección')
        return redirect(url_for('inicio.index'))


#Vista para asignar docente a un curso
@cursos.route('/cursos-docente')
@login_required
def asignar_docente():
    # cursos 
    curso = Curso()
    cursos = curso.obtener_cursos(current_user.id_cliente)
    # docentes
    docente = Docente()
    docentes = docente.obtenerDocentesCliente(current_user.id_cliente)
    # Listas para almacenar los cursos y docentes activos
    lista_curso_activos = []
    lista_docentes_activos = []
    for curso_lista in cursos:
        if curso.lista_curso_docente(curso_lista[0], current_user.id_cliente) == None:
            if curso_lista[14] == 1:
                lista_curso_activos.append(curso_lista)
        else:
            pass
    for docente_lista in docentes:
        if docente_lista[7] == 1:
            lista_docentes_activos.append(docente_lista)
        else:
            pass
    print(lista_curso_activos)
    return render_template('cursoxdocente.html', cursos=lista_curso_activos, docentes=lista_docentes_activos)
@cursos.route('/asignar_docente', methods=['POST', 'GET'])
@login_required
def asignar_docente_curso():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        id_docente = request.form['id_docente']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        if id_curso and id_docente and fecha_inicio and fecha_fin:
            curso = Curso()
            if curso.asignar_docente_curso(id_curso, id_docente, current_user.id_cliente, fecha_inicio, fecha_fin):
                flash('Docente asignado correctamente')
                return redirect(url_for('cursos.asignar_docente'))
            else:
                flash('Error al asignar docente')
                return redirect(url_for('cursos.asignar_docente'))
        else:
            flash('Por favor, complete los campos')
            return redirect(url_for('cursos.asignar_docente'))
    else:
        flash('Error al asignar docente')
        return redirect(url_for('cursos.asignar_docente'))





@cursos.route("/actualizar-curso", methods=['POST'])
@login_required
def actualizar_curso():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        nombre_curso = request.form['nombre_curso']
        codigo_curso = request.form['codigo_curso']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_finalizacion']
        horario = request.form['horario']
        duracion = request.form['duracion']
        intensidad_horaria = request.form['intensidad_horaria']
        cantidad_sesiones  = request.form['cantidad_sesiones']
        cupo = request.form['cupo']
        enlace_clase = request.form['enlace_clase']
        enlace_grabacion = request.form['enlace_grabacion']
        enlace_formulario = request.form['enlace_formulario']
        print(id_curso, nombre_curso, codigo_curso, fecha_inicio, fecha_fin, horario, duracion, intensidad_horaria, cantidad_sesiones, cupo, enlace_clase, enlace_grabacion, enlace_formulario)
        if id_curso and nombre_curso and codigo_curso and fecha_inicio and fecha_fin and horario and duracion and intensidad_horaria and cantidad_sesiones and cupo and enlace_clase and enlace_grabacion and enlace_formulario:
            curso = Curso(nombre_curso=nombre_curso, codigo_curso=codigo_curso, fecha_incio=fecha_inicio, fecha_fin=fecha_fin, horario=horario, duracion=duracion, intensidad_horaria=intensidad_horaria, cantidad_sesiones=cantidad_sesiones, cupo_curso=cupo, enlace_clase=enlace_clase, enlace_grabaciones=enlace_grabacion, enlace_form_asistencia=enlace_formulario)
            if curso.actualizar_curso(id_curso):
                flash('Curso actualizado correctamente')
                return redirect(url_for('cursos.listar_cursos'))
            else:
                flash('Error al actualizar curso')
                return redirect(url_for('cursos.listar_cursos'))


        

       





##########################################################################
# --------------------- Rutas para la consulta ajax -------------------- #
##########################################################################

# Ruta para consultar la información de un curso
@cursos.route('/consultar-curso/modal', methods=['POST'])
@login_required
def consultar_curso():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        curso = Curso()
        curso = curso.obtener_curso(id_curso)
        date_format = "%Y-%m-%d"
        curso_json = {
            'nombre_curso': curso[1],
            'codigo_curso': curso[2],
            'fecha_inicio': curso[3].strftime(date_format),
            'fecha_fin': curso[4].strftime(date_format),
            'horario': curso[5],
            'modalidad': curso[6],
            'duracion': curso[7],
            'intensidad_horaria': curso[8],
            'cantidad_sesiones': curso[9],
            'cupo_curso': curso[10],
            'enlace_clase': curso[11],
            'enlace_grabaciones': curso[12],
            'enlace_asistencia': curso[13]
        }
        return curso_json
    else:
        return 'Error al consultar curso'

# Generar informe de asistencia y calificaciones en un archivo de excel.
@cursos.route('/generar-informe', methods=['POST'])
def generar_informe():
    if request.method == 'POST':
        salida = io.BytesIO()
        id_curso = request.form['id_curso']
        curso = Curso()
        curso = curso.obtener_curso(id_curso)
        # obtener la asistencia de los estudiantes y las calificaciones
        estudiante=Estudiante()
        #se obtiene las asistencuas y calificaciones de los estudiantes
        # se obtiene el id del estudiante y se envia como parametro para obtener la asistencia y calificaciones
        asistencia=estudiante.obtener_asistencia(id_curso)
        calificaciones=estudiante.obtener_calificacion(id_curso)
    #    Obtener numero de documento y nombre del estudiante
        estudiantes=estudiante.obtener_estudiantes(id_curso)
        # se crea el archivo excel
        workbook = xlsxwriter.Workbook(salida)
        # se crea una hoja de calculo
        worksheet = workbook.add_worksheet()
        # se crea un formato para las celdas
        formato_celda = workbook.add_format(
            {'bold': True, 'font_color': 'white', 'bg_color': '#1E90FF', 'align': 'center', 'valign': 'vcenter', 'border': 1})

        # se agrega la información
        worksheet.write('A1', 'Nombre del curso', formato_celda)
        worksheet.write('B1', curso[1], formato_celda)
        worksheet.write('A2', 'Codigo del curso', formato_celda)
        worksheet.write('B2', curso[2], formato_celda)
        worksheet.write('A3', 'Fecha de inicio', formato_celda)
        worksheet.write('B3', curso[3], formato_celda)
        worksheet.write('A4', 'Fecha de finalización', formato_celda)
        worksheet.write('B4', curso[4], formato_celda)
        worksheet.write('A5', 'Horario', formato_celda)
        worksheet.write('B5', curso[5], formato_celda)
        worksheet.write('A6', 'Modalidad', formato_celda)
        worksheet.write('B6', curso[6], formato_celda)
        worksheet.write('A7', 'Duración', formato_celda)
        worksheet.write('B7', curso[7], formato_celda)
        worksheet.write('A8', 'Intensidad horaria', formato_celda)
        worksheet.write('B8', curso[8], formato_celda)
        worksheet.write('A9', 'Cantidad de sesiones', formato_celda)
        worksheet.write('B9', curso[9], formato_celda)
        worksheet.write('A10', 'Cupo del curso', formato_celda)
        worksheet.write('B10', curso[10], formato_celda)
        worksheet.write('A11', 'Enlace de la clase', formato_celda)
        worksheet.write('B11', curso[11], formato_celda)
        worksheet.write('A12', 'Enlace de las grabaciones', formato_celda)
        worksheet.write('B12', curso[12], formato_celda)
        worksheet.write('A13', 'Enlace de asistencia', formato_celda)
        worksheet.write('B13', curso[13], formato_celda)
        worksheet.write('A14', 'Número de documento', formato_celda)
        worksheet.write('B14', 'Nombre del estudiante', formato_celda)
        worksheet.write('C14', 'Asistencia', formato_celda)
        worksheet.write('D14', 'Calificación', formato_celda)
        # se agregan los estudiantes
        fila = 15
        for estudiante in estudiantes:
            worksheet.write('A' + str(fila), estudiante[0], formato_celda)
            worksheet.write('B' + str(fila + 1), estudiante[1], formato_celda)
            fila += 1
        # se agregan las asistencias
        fila = 15
        for asistencia in asistencia:
            worksheet.write('C' + str(fila), asistencia[0], formato_celda)
            fila += 1
        # se agregan las calificaciones
        fila = 15
        for calificacion in calificaciones:
            worksheet.write('D' + str(fila), calificacion[0], formato_celda)
            fila += 1
        # se cierra el archivo
        workbook.close()
        # se retorna el archivo
        salida.seek(0)
        return Response(salida, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        return 'Error al generar informe'

        







        

        


        


  
