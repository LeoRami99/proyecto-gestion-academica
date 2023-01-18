import io
from time import strftime
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, Response, send_file
from flask_login import login_required, current_user
from .curso import Curso
from app.docentes.docente import Docente
from app.estudiantes.estudiante import Estudiante
import xlwt


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
        # contador de estudiantes por curso
        estudiante = Estudiante()
        
        # Condición para verificar si se asigno el docente al curso
        lista_cursos = []
        for curso_lista in cursos:
            if curso.lista_curso_docente(curso_lista[0], current_user.id_cliente) != None:
                # Se agrega el curso + el nombre del docente
                cursoxdocente = docente.obtenerDocente(curso.lista_curso_docente(curso_lista[0], current_user.id_cliente)[3])
                docente_nombre_apellido = cursoxdocente[2] + ' ' + cursoxdocente[3] 
                # agregar el contador de estudiantes por curso
                contador_estudiantes = estudiante.count_usuarios_cupo(curso_lista[0], current_user.id_cliente)
                lista_cursos.append(curso_lista + (docente_nombre_apellido, contador_estudiantes))
            else:
                contador_estudiantes = estudiante.count_usuarios_cupo(curso_lista[0], current_user.id_cliente)
                # Se agrega el curso + sin asignar
                lista_cursos.append(curso_lista + ('Sin asignar', contador_estudiantes))
        return render_template('cursos_index.html', cursos=lista_cursos, docentes=docentes)
    elif current_user.rol == 'DOC':
        estudiante= Estudiante()
        #Solo listar los cursos que se le fueron asignados a el docente
        curso = Curso()
        asig_doc = curso.obtener_cursos_docente(current_user.id)
        cursos = curso.obtener_cursos(current_user.id_cliente)
        listar_cursos = []
        for cursos in zip(cursos, asig_doc):
            contador_estudiantes = estudiante.count_usuarios_cupo(cursos[0][0], current_user.id_cliente)
            if cursos[1] != None:
                listar_cursos.append(cursos[0]+(contador_estudiantes,))
            else:
                pass
        print(listar_cursos)
        return render_template('cursos_index.html', cursos=listar_cursos)
    else:
        flash('No tiene permisos para acceder a esta sección')
        return redirect(url_for('inicio.index'))

@cursos.route('/cursos-no-activos')
@login_required
def cursos_no_activos():
    if current_user.rol == 'AD':
        curso = Curso()
        cursos = curso.obtener_cursos(current_user.id_cliente)
        # Datos del docente
        docente = Docente()
        docentes = docente.obtenerDocentesCliente(current_user.id_cliente)
        # contador de estudiantes por curso
        estudiante = Estudiante()
        
        # Condición para verificar si se asigno el docente al curso
        lista_cursos = []
        for curso_lista in cursos:
            if curso.lista_curso_docente(curso_lista[0], current_user.id_cliente) != None:
                # Se agrega el curso + el nombre del docente
                cursoxdocente = docente.obtenerDocente(curso.lista_curso_docente(curso_lista[0], current_user.id_cliente)[3])
                docente_nombre_apellido = cursoxdocente[2] + ' ' + cursoxdocente[3] 
                # agregar el contador de estudiantes por curso
                contador_estudiantes = estudiante.count_usuarios_cupo(curso_lista[0], current_user.id_cliente)
                lista_cursos.append(curso_lista + (docente_nombre_apellido, contador_estudiantes))
            else:
                contador_estudiantes = estudiante.count_usuarios_cupo(curso_lista[0], current_user.id_cliente)
                # Se agrega el curso + sin asignar
                lista_cursos.append(curso_lista + ('Sin a s zsignar', contador_estudiantes))
        return render_template('cursos_noactivos.html', cursos=lista_cursos, docentes=docentes)
   

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
@cursos.route("/estado-curso", methods=['POST'])
@login_required
def estado_curso():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        if id_curso:
            curso = Curso()
            if curso.estado_curso(id_curso, current_user.id_cliente):
                if curso.cerrar_curso(id_curso, current_user.id_cliente):
                   flash('Curso cerrado correctamente')
                   return redirect(url_for('cursos.listar_cursos'))
                else:
                    flash('Error al cerrar curso')
                    return redirect(url_for('cursos.listar_cursos'))
            else:
                flash('Verifica las notas y calificaciones de los estudiantes, antes de dar por finalizado el curso')
                return redirect(url_for('cursos.listar_cursos'))
        else:
            flash('Error al cerrar curso')
            return redirect(url_for('cursos.listar_cursos'))
    else:
        flash('Error al cerrar curso')
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
        try:
            salida = io.BytesIO()
            libro = xlwt.Workbook()
            id_curso = request.form['id_curso']
            curso = Curso()
            curso = curso.obtener_curso(id_curso)
            # colocar información del curso en la hoja
            nombre_curso = curso[1]
            codigo_curso = curso[2]
            fecha_inicio = curso[3].strftime("%d/%m/%Y")
            fecha_fin = curso[4].strftime("%d/%m/%Y")
            horario = str(curso[5])
            modalidad = str(curso[6])
            duracion = str(curso[7])
            intensidad_horaria = str(curso[8])
            cantidad_sesiones = str(curso[9])
            cupo_curso = str(curso[10])
            enlace_clase = str(curso[11])
            enlace_grabaciones = str(curso[12])
            enlace_asistencia = str(curso[13])
            #estilo_inf_curso de fecha
            

            # Obtener información de los estudiantes
            # Agregar formato de tabla a la hoja de excel con la información del curso y agregar todos los bordes a las celdas y fondo de color gris

            estilo_inf_curso = xlwt.easyxf('font: bold 1, color black; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_colour gray25; borders: left thin, right thin, top thin, bottom thin;')
            # Colocar todos los bordes a las celdas y centrar el texto
            estilo_texto = xlwt.easyxf('align: wrap on, vert centre, horiz center; borders: left thin, right thin, top thin, bottom thin;')

            hoja = libro.add_sheet(nombre_curso)
            hoja.write(0, 0, 'Nombre del curso', estilo_inf_curso)
            hoja.write(0, 1, nombre_curso, estilo_texto)
            hoja.write(1, 0, 'Código del curso', estilo_inf_curso)
            hoja.write(1, 1, codigo_curso, estilo_texto)
            hoja.write(2, 0, 'Fecha de inicio', estilo_inf_curso)
            hoja.write(2, 1, fecha_inicio, estilo_texto)
            hoja.write(3, 0, 'Fecha de finalización', estilo_inf_curso)
            hoja.write(3, 1, fecha_fin, estilo_texto)
            hoja.write(4, 0, 'Horario', estilo_inf_curso)
            hoja.write(4, 1, horario, estilo_texto)
            hoja.write(5, 0, 'Modalidad', estilo_inf_curso)
            hoja.write(5, 1, modalidad, estilo_texto)
            hoja.write(6, 0, 'Duración', estilo_inf_curso)
            hoja.write(6, 1, duracion, estilo_texto)
            hoja.write(7, 0, 'Intensidad horaria', estilo_inf_curso)
            hoja.write(7, 1, intensidad_horaria, estilo_texto)
            hoja.write(8, 0, 'Cantidad de sesiones', estilo_inf_curso)
            hoja.write(8, 1, cantidad_sesiones, estilo_texto)
            hoja.write(9, 0, 'Cupo del curso', estilo_inf_curso)
            hoja.write(9, 1, cupo_curso, estilo_texto)
            hoja.write(10, 0, 'Enlace de la clase', estilo_inf_curso)
            hoja.write(10, 1, enlace_clase, estilo_texto)
            hoja.write(11, 0, 'Enlace de las grabaciones', estilo_inf_curso)
            hoja.write(11, 1, enlace_grabaciones, estilo_texto)
            hoja.write(12, 0, 'Enlace del formulario de asistencia', estilo_inf_curso)
            hoja.write(12, 1, enlace_asistencia, estilo_texto)

            # estilo de formato de tabla con las calificaciones y asistencias
            estilo_tabla = xlwt.easyxf('align: wrap on, vert centre, horiz center; borders: left thin, right thin, top thin, bottom thin;')
            hoja.write(14, 0, '#', estilo_tabla)
            hoja.write(14, 1, 'Número de documento', estilo_tabla)
            hoja.write(14, 2, 'Nombres', estilo_tabla)
            hoja.write(14, 3, 'Apellidos', estilo_tabla)
            hoja.write(14, 4, 'Calificación 1', estilo_tabla)
            hoja.write(14, 5, 'Calificación 2', estilo_tabla)
            hoja.write(14, 6, 'Calificación 3', estilo_tabla)
            hoja.write(14, 7, 'Calificación 4', estilo_tabla)
            hoja.write(14, 8, 'Calificación 5', estilo_tabla)
            hoja.write(14, 9, 'Calificación 6', estilo_tabla)
            hoja.write(14, 10, 'Calificación 7', estilo_tabla)
            hoja.write(14, 11, 'Calificación 8', estilo_tabla)
            hoja.write(14, 12, 'Calificación 9', estilo_tabla)
            hoja.write(14, 13, 'Calificación final', estilo_tabla)
            hoja.write(14, 14, 'Observaciones', estilo_tabla)
            hoja.write(14, 15, 'Asistencia 1', estilo_tabla)
            hoja.write(14, 16, 'Asistencia 2', estilo_tabla)
            hoja.write(14, 17, 'Asistencia 3', estilo_tabla)
            hoja.write(14, 18, 'Asistencia 4', estilo_tabla)
            hoja.write(14, 19, 'Asistencia 5', estilo_tabla)
            hoja.write(14, 20, 'Asistencia 6', estilo_tabla)
            hoja.write(14, 21, 'Asistencia 7', estilo_tabla)
            hoja.write(14, 22, 'Asistencia 8', estilo_tabla)
            hoja.write(14, 23, 'Asistencia 9', estilo_tabla)
            hoja.write(14, 24, 'Asistencia 10', estilo_tabla)
            hoja.write(14, 25, 'Asistencia 11', estilo_tabla)
            hoja.write(14, 26, 'Asistencia 12', estilo_tabla)
            hoja.write(14, 27, 'Asistencia 13', estilo_tabla)
            hoja.write(14, 28, 'Asistencia 14', estilo_tabla)
            hoja.write(14, 29, 'Asistencia 15', estilo_tabla)
            hoja.write(14, 30, 'Asistencia 16', estilo_tabla)
            hoja.write(14, 31, 'Asistencia 17', estilo_tabla)
            hoja.write(14, 32, 'Asistencia 18', estilo_tabla)
            hoja.write(14, 33, 'Asistencia 19', estilo_tabla)
            hoja.write(14, 34, 'Asistencia 20', estilo_tabla)
            hoja.write(14, 35, 'Asistencia 21', estilo_tabla)
            hoja.write(14, 36, 'Asistencia 22', estilo_tabla)
            hoja.write(14, 37, 'Asistencia 23', estilo_tabla)
            hoja.write(14, 38, 'Asistencia 24', estilo_tabla)
            hoja.write(14, 39, 'Asistencia 25', estilo_tabla)
            hoja.write(14, 40, 'Asistencia 26', estilo_tabla)
            hoja.write(14, 41, 'Asistencia 27', estilo_tabla)
            hoja.write(14, 42, 'Asistencia 28', estilo_tabla)
            hoja.write(14, 43, 'Asistencia 29', estilo_tabla)
            hoja.write(14, 44, 'Asistencia 30', estilo_tabla)

            calificacion = Estudiante().obtener_calificacion(id_curso)
            asistencia = Estudiante().obtener_asistencia(id_curso)

            matriz_calificacion_asistencia = []
            for indice in zip(calificacion, asistencia):
                matriz_calificacion_asistencia.append(indice)
            
            
            for fila, (calificacion, asistencia) in enumerate(matriz_calificacion_asistencia):
                hoja.write(fila+15, 0, fila+1, estilo_tabla)
                hoja.write(fila+15, 1, str(calificacion[0]), estilo_tabla)
                hoja.write(fila+15, 2, str(calificacion[1]), estilo_tabla)
                hoja.write(fila+15, 3, str(calificacion[2]), estilo_tabla)
                hoja.write(fila+15, 4, str(calificacion[3]), estilo_tabla)
                hoja.write(fila+15, 5, str(calificacion[4]), estilo_tabla)
                hoja.write(fila+15, 6, str(calificacion[5]), estilo_tabla)
                hoja.write(fila+15, 7, str(calificacion[6]), estilo_tabla)
                hoja.write(fila+15, 8, str(calificacion[7]), estilo_tabla)
                hoja.write(fila+15, 9, str(calificacion[8]), estilo_tabla)
                hoja.write(fila+15, 10, str(calificacion[9]), estilo_tabla)
                hoja.write(fila+15, 11, str(calificacion[10]), estilo_tabla)
                hoja.write(fila+15, 12, str(calificacion[11]), estilo_tabla)
                hoja.write(fila+15, 13, str(calificacion[12]), estilo_tabla)
                hoja.write(fila+15, 14, str(calificacion[13]), estilo_tabla)
                hoja.write(fila+15, 15, str(asistencia[3]), estilo_tabla)
                hoja.write(fila+15, 16, str(asistencia[4]), estilo_tabla)
                hoja.write(fila+15, 17, str(asistencia[5]), estilo_tabla)
                hoja.write(fila+15, 18, str(asistencia[6]), estilo_tabla)
                hoja.write(fila+15, 19, str(asistencia[7]), estilo_tabla)
                hoja.write(fila+15, 20, str(asistencia[8]), estilo_tabla)
                hoja.write(fila+15, 21, str(asistencia[9]), estilo_tabla)
                hoja.write(fila+15, 22, str(asistencia[10]), estilo_tabla)
                hoja.write(fila+15, 23, str(asistencia[11]), estilo_tabla)
                hoja.write(fila+15, 24, str(asistencia[12]), estilo_tabla)
                hoja.write(fila+15, 25, str(asistencia[13]), estilo_tabla)
                hoja.write(fila+15, 26, str(asistencia[14]), estilo_tabla)
                hoja.write(fila+15, 27, str(asistencia[15]), estilo_tabla)
                hoja.write(fila+15, 28, str(asistencia[16]), estilo_tabla)
                hoja.write(fila+15, 29, str(asistencia[17]), estilo_tabla)
                hoja.write(fila+15, 30, str(asistencia[18]), estilo_tabla)
                hoja.write(fila+15, 31, str(asistencia[19]), estilo_tabla)
                hoja.write(fila+15, 32, str(asistencia[20]), estilo_tabla)
                hoja.write(fila+15, 33, str(asistencia[21]), estilo_tabla)
                hoja.write(fila+15, 34, str(asistencia[22]), estilo_tabla)
                hoja.write(fila+15, 35, str(asistencia[23]), estilo_tabla)
                hoja.write(fila+15, 36, str(asistencia[24]), estilo_tabla)
                hoja.write(fila+15, 37, str(asistencia[25]), estilo_tabla)
                hoja.write(fila+15, 38, str(asistencia[26]), estilo_tabla)
                hoja.write(fila+15, 39, str(asistencia[27]), estilo_tabla)
                hoja.write(fila+15, 40, str(asistencia[28]), estilo_tabla)
                hoja.write(fila+15, 41, str(asistencia[29]), estilo_tabla)
                hoja.write(fila+15, 42, str(asistencia[30]), estilo_tabla)
                hoja.write(fila+15, 43, str(asistencia[31]), estilo_tabla)
                hoja.write(fila+15, 44, str(asistencia[32]), estilo_tabla)
                
            
        
            libro.save(salida)

            salida.seek(0)
            flash('Informe generado con exito')
            return Response(salida, mimetype='application/vnd.ms-excel', headers={'Content-Disposition':'attachment;filename=informe_'+nombre_curso+'.xls'})
        except Exception as e:
            flash('Error al generar el reporte')
            return redirect(url_for('cursos.listar_cursos'))
    else:
        return redirect(url_for('cursos.listar_cursos'))

        
