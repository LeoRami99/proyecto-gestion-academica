from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
#Importación de la clase Curso
from app.cursos.curso import Curso
# Clase de metodos de enviar a la base de datos
from app.estudiantes.estudiante import Estudiante

# Se importa pandas para leer el excel
import pandas as pd



estudiantes = Blueprint('estudiantes', __name__, template_folder='templates', url_prefix='/')

@estudiantes.route('/estudiantes')
@login_required
def index():
    return render_template('estudiantes.html')
@estudiantes.route('/registro-estudiantes')
@login_required
def registro_estudiantes():
    cursos = Curso().obtener_cursos(current_user.id_cliente)
    return render_template('registro-estudiantes.html', cursos=cursos)
@estudiantes.route('/guardar-estudiante', methods=['POST'])
@login_required
def guardar_estudiante():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        tipo_doc = request.form['tipo_doc']
        num_doc = request.form['num_doc']
        correo = request.form['correo']
        telefono = request.form['telefono']
        tel_fijo = request.form['tel_fijo']
        ciudad = request.form['ciudad']
        id_curso = request.form['id_curso']
        if nombres and apellidos and tipo_doc and num_doc and correo and telefono and tel_fijo and ciudad:
            estudiante = Estudiante(nombres, apellidos, tipo_doc, num_doc, correo, telefono, tel_fijo, ciudad, current_user.id_cliente, "1")
            if Estudiante.verificacion_estudiantes(num_doc, current_user.id_cliente):
                flash('El estudiante ya se encuentra registrado')
                return redirect(url_for('estudiantes.registro_estudiantes'))
            else:
                if estudiante.guardar_estudiante():
                    # verificar si el estudiante se registro correctamente
                    if Estudiante.verificacion_estudiantes(num_doc, current_user.id_cliente):
                        # Se obtiene el id del estudiante
                        id_estudiante = Estudiante.estudiante_id(num_doc, current_user.id_cliente)

                        # Se registra el estudiante en el curso
                        if Estudiante.asignar_estudiante_curso(id_curso, id_estudiante, current_user.id_cliente, datetime.now(), datetime.now()):
                            if Estudiante.generar_info_asistencia(id_estudiante, id_curso, current_user.id_cliente) and Estudiante.generar_info_calificaciones(id_estudiante, id_curso, current_user.id_cliente):
                                flash('El estudiante se registro correctamente')
                                return redirect(url_for('estudiantes.registro_estudiantes'))
                            else:
                                flash("Ocurrio un error al registrar el estudiante")
                                return redirect(url_for('estudiantes.registro_estudiantes'))
                        else:
                            flash('No se pudo registrar el estudiante')
                            return redirect(url_for('estudiantes.registro_estudiantes'))

                       
                    else:
                        flash('No se pudo registrar el estudiante')
                        return redirect(url_for('estudiantes.registro_estudiantes'))

                else:
                    flash('No se pudo registrar el estudiante')
                    return redirect(url_for('estudiantes.registro_estudiantes'))
        else:
            flash('Todos los campos son obligatorios')
            return redirect(url_for('estudiantes.registro_estudiantes'))
    else:
        flash('No se pudo registrar el estudiante')
        return redirect(url_for('estudiantes.registro_estudiantes'))

# excel con registro de estudiantes
@estudiantes.route('/estudiantes-excel', methods=['POST'])
@login_required
def estudiantes_excel():
    if request.method == 'POST':
        # Se obtiene el excel del formulario
        excel = request.files['excel']
        id_curso = request.form['id_curso']
        # verificar que el archivo sea un excel
        try:
            if not excel.filename.endswith('.xlsx'):
                flash('El archivo no es un excel')
                return redirect(url_for('estudiantes.registro_estudiantes'))
            else:
                # Se lee el excel con pandas
                df = pd.read_excel(excel)
                # Se obtiene el nombre de las columnas
                columnas = df.columns
                # Recorreror las columnas y enviar la información
                for index, row in df.iterrows():
                #Verificar que el estudiante no se encuentre previamente registrado y omitir el la columna
                    if Estudiante().verificacion_estudiantes(row[columnas[3]], current_user.id_cliente) == False:
                        estudiante = Estudiante(row[columnas[0]], row[columnas[1]], row[columnas[2]], row[columnas[3]], row[columnas[4]], row[columnas[5]], row[columnas[6]], row[columnas[7]], current_user.id_cliente, "1")
                        if estudiante.guardar_estudiante():
                            # verificar si el estudiante se registro correctamente
                            if Estudiante.verificacion_estudiantes(row[columnas[3]], current_user.id_cliente):
                                # Se obtiene el id del estudiante
                                id_estudiante = Estudiante.estudiante_id(row[columnas[3]], current_user.id_cliente)

                                # Se registra el estudiante en el curso
                                if Estudiante.asignar_estudiante_curso(id_curso, id_estudiante, current_user.id_cliente, datetime.now(), datetime.now()):
                                    if Estudiante.generar_info_asistencia(id_estudiante, id_curso, current_user.id_cliente) and Estudiante.generar_info_calificaciones(id_estudiante, id_curso, current_user.id_cliente):
                                        pass
                                    else:
                                        flash("Ocurrio un error al registrar el estudiante")
                                        return redirect(url_for('estudiantes.registro_estudiantes'))
                                else:
                                    flash('No se pudo registrar el estudiante')
                                    return redirect(url_for('estudiantes.registro_estudiantes'))

                            flash('El estudiante ' + str(row[columnas[3]]) + ' se registro correctamente')
                            pass
                        else:
                            pass
                    else:
                        flash('Ya se encuentra registrado ' + str(row[columnas[3]]))
                        pass
                return redirect(url_for('estudiantes.registro_estudiantes'))
        except Exception as e:
            print(e)
            flash('No se pudo procesar el excel, verifica el formato de las columnas')
            return redirect(url_for('estudiantes.registro_estudiantes'))

    else:
        flash('No se pudo registrar el estudiante')
        return redirect(url_for('estudiantes.registro_estudiantes'))

# Estudiantes por curso
@estudiantes.route('/estudiantes-curso')
@login_required
def estudiantes_curso():
    cursos = Curso()
    estudiantes = Estudiante()
    cursos = cursos.obtener_cursos(current_user.id_cliente)
    curso_lista = []
    contado_estudiantes = []
    for curso in cursos:
        if curso[14] == 1:  
            contado_estudiantes.append(str(estudiantes.count_usuarios_cupo(curso[0], current_user.id_cliente)))
            curso_lista.append(curso)
        else:
            pass
    curso_lista = zip(curso_lista, contado_estudiantes)

    return render_template('estudiantesxcurso.html', cursos=curso_lista)




    # return render_template('estudiantesxcurso.html', cursos=cursos)


# asignar estudiantes al curso
@estudiantes.route('/asignar-estudiantes', methods=['POST'])
@login_required
def asignar_estudiantes():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin   = request.form['fecha_fin']
        num_doc = request.form['num_doc']

        if id_curso and num_doc:
            curso_indice = Curso()
            estudiantes = Estudiante()
            lista_estudiantes=[]
            # Se obtiene el cupo del curso  
            if estudiantes.verificacion_estudiantes(num_doc, current_user.id_cliente):
                id_estudiante = estudiantes.estudiante_id(num_doc, current_user.id_cliente)
                if id_estudiante>0:
                    if estudiantes.asignar_estudiante_curso(id_curso, id_estudiante, current_user.id_cliente, fecha_inicio, fecha_fin):
                        estudiantes.generar_info_asistencia(id_estudiante, id_curso, current_user.id_cliente)
                        estudiantes.generar_info_calificaciones(id_estudiante, id_curso, current_user.id_cliente)
                        flash('El estudiante se asigno correctamente')
                        return redirect(url_for('estudiantes.estudiantes_curso'))
                    else:
                        flash('No se pudo asignar el estudiante')
                        return redirect(url_for('estudiantes.estudiantes_curso'))
            else:
                flash('El estudiante no se encuentra registrado')
                return redirect(url_for('estudiantes.estudiantes_curso'))
        else:
            flash('No se pudo asignar el estudiante')
            return redirect(url_for('estudiantes.estudiantes_curso'))
    else:
        flash('No se pudo asignar el estudiante')
        return redirect(url_for('estudiantes.estudiantes_curso'))        

# Estudiantes por curso con archivo de excel
@estudiantes.route('/estudiantes-curso-excel', methods=['POST'])
@login_required
def estudiantes_curso_excel():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin   = request.form['fecha_fin']
        try:
            # Se obtiene el excel del formulario
            excel = request.files['excel']
            # verificar que el archivo sea un excel
            if not excel.filename.endswith('.xlsx'):
                flash('El archivo no es un excel')
                return redirect(url_for('estudiantes.estudiantes_curso'))
            else:
                # Se lee el excel con pandas
                df = pd.read_excel(excel)
                # Se obtiene el nombre de las columnas
                columnas = df.columns
                numero_de_filas = df.count()
                # Se trae cupo del curso de la base de datos
                curso_indice = Curso()
                print("Número de filas", numero_de_filas.values[0])
                if numero_de_filas.values[0] == curso_indice.obtener_curso(id_curso)[10]:
                    # Recorreror las columnas y enviar la información
                    for index, row in df.iterrows():
                        #Verificar que el estudiante no se encuentre previamente registrado y omitir el la columna
                        estudiante = Estudiante()
                        if estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente) != False:
                            if estudiante.asignar_estudiante_curso(id_curso, estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente), current_user.id_cliente, fecha_inicio, fecha_fin) and estudiante.generar_info_asistencia(estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente), id_curso, current_user.id_cliente) and estudiante.generar_info_calificaciones(estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente), id_curso, current_user.id_cliente):
                                flash('El estudiante ' + str(row[columnas[0]]) + ' se asigno correctamente ')
                                pass
                            else:
                                pass
                        else:
                            flash('El estudiante ' + str(row[columnas[1]]) + ' no se encuentra registrado')
                            pass
                    
                    return redirect(url_for('estudiantes.estudiantes_curso'))
                else:
                    flash('El número de estudiantes en el excel no coincide con el cupo del curso')
                    return redirect(url_for('estudiantes.estudiantes_curso'))
        except Exception as e:
            print(e)
            flash('No se pudo procesar el excel, verifica el formato de las columnas')
            return redirect(url_for('estudiantes.estudiantes_curso'))

#Asistencia de estudiantes
@estudiantes.route('/asistencia-notas')
@login_required
def asistencia_estudiantes():
    curso = Curso()
    
    cursos =curso.obtener_cursos(current_user.id_cliente)
    # Solo va a mostrar los cursos activos
    asig_doc = curso.obtener_cursos_docente(current_user.id)
    lista_cursos_activos=[]
    if current_user.rol == "AD":
        for indice in curso.obtener_cursos(current_user.id_cliente):
            if indice[14]==1:
                lista_cursos_activos.append(indice)
            else:
                pass
    else:
        # mostrar al docente los cursos que tiene asignados
       for list_curso_doc in zip(cursos, asig_doc):
            if list_curso_doc[0][14]==1:
                if list_curso_doc[0][0]==list_curso_doc[1][1]:
                   lista_cursos_activos.append(list_curso_doc[0])
                else:
                    pass
            else:
                pass

    return render_template('asistencia_calificacion.html', cursos=lista_cursos_activos)

            
    # return render_template('asistencia_calificacion.html', cursos=lista_cursos_activos)
@estudiantes.route('/asistencia-estudiantes/<id_curso>')
@login_required
def asistencia_estudiantes_id(id_curso):
    estudiante = Estudiante()
    lista_asistencia = estudiante.obtener_asistencia_curso(id_curso, current_user.id_cliente)
    lista_estudiante_asistencia=[]
    for indice in lista_asistencia:
        # reemplazar el id del del estudiante por el nombre y el apellido y agregar el numero de documento
        estudiante_info = estudiante.obtener_estudiante(indice[1])
        # print("id del estudiante",indice[0])
        lista_estudiante_asistencia.append(estudiante_info+indice[4:34])
        
    return render_template('asistencia.html', asistencia=lista_estudiante_asistencia, id_curso=id_curso)

@estudiantes.route('/enviar-asistencia', methods=['POST'])
@login_required
def enviar_asistencia():
    if request.method == 'POST':
        estudiante = Estudiante()
        id_curso = request.form['id_curso']
        
        lista_asistencias = []
        lista_asistencias.append(request.form.getlist('num_doc'))
        
        for indice in range(30):
           lista_asistencias.append(request.form.getlist('asistencia_'+str(indice+1)))
        # se envia a la base de datos
        estudiante = Estudiante()
        # print(lista_asistencias[0])
        for indice in range(len(lista_asistencias[0])):
            

            # Condifición con 33 datos para el envio de información
            if estudiante.actualizar_asistencia(estudiante.estudiante_id(lista_asistencias[0][indice], current_user.id_cliente), current_user.id_cliente, id_curso, lista_asistencias[1][indice], lista_asistencias[2][indice], lista_asistencias[3][indice], lista_asistencias[4][indice], lista_asistencias[5][indice], lista_asistencias[6][indice], lista_asistencias[7][indice], lista_asistencias[8][indice], lista_asistencias[9][indice], lista_asistencias[10][indice], lista_asistencias[11][indice], lista_asistencias[12][indice], lista_asistencias[13][indice], lista_asistencias[14][indice], lista_asistencias[15][indice], lista_asistencias[16][indice], lista_asistencias[17][indice], lista_asistencias[18][indice], lista_asistencias[19][indice], lista_asistencias[20][indice], lista_asistencias[21][indice], lista_asistencias[22][indice], lista_asistencias[23][indice], lista_asistencias[24][indice], lista_asistencias[25][indice], lista_asistencias[26][indice], lista_asistencias[27][indice], lista_asistencias[28][indice], lista_asistencias[29][indice], lista_asistencias[30][indice]) == True:
                # print((lista_asistencias[0][indice], current_user.id_cliente), id_curso, current_user.id_cliente, lista_asistencias[1][indice], lista_asistencias[2][indice], lista_asistencias[3][indice], lista_asistencias[4][indice], lista_asistencias[5][indice], lista_asistencias[6][indice], lista_asistencias[7][indice], lista_asistencias[8][indice], lista_asistencias[9][indice], lista_asistencias[10][indice], lista_asistencias[11][indice], lista_asistencias[12][indice], lista_asistencias[13][indice], lista_asistencias[14][indice], lista_asistencias[15][indice], lista_asistencias[16][indice], lista_asistencias[17][indice], lista_asistencias[18][indice], lista_asistencias[19][indice], lista_asistencias[20][indice], lista_asistencias[21][indice], lista_asistencias[22][indice], lista_asistencias[23][indice], lista_asistencias[24][indice], lista_asistencias[25][indice], lista_asistencias[26][indice], lista_asistencias[27][indice], lista_asistencias[28][indice], lista_asistencias[29][indice], lista_asistencias[30][indice])
                flash('Se actualizo la asistencia del estudiante ' + str(lista_asistencias[0][indice]))
                pass
            else:
                flash('No se actualizo la asistencia del estudiante ' + str(lista_asistencias[0][indice]))
                pass
        return redirect(url_for('estudiantes.asistencia_estudiantes_id', id_curso=id_curso))
    else:
        flash('No se actualiza la asistencia')
        return redirect(url_for('estudiantes.asistencia_estudiantes'))
@estudiantes.route('/enviar-asistencia-excel', methods=['POST'])
@login_required
def enviar_asistencia_excel():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        try:
            excel = request.files['excel']
            if not excel.filename.endswith('.xlsx'):
                flash('No se selecciono ningun archivo, primera condición')
                return redirect(url_for('estudiantes.asistencia_estudiantes_id', id_curso=id_curso))
            else:
                # se lee el archivo con las asistencias del estudiante
                df = pd.read_excel(excel)
                # se envia a la base de datos
                columnas = df.columns
                estudiante = Estudiante()
                for indice in range(len(df)):
                    # Condifición con 33 datos para el envio de información
                    if estudiante.actualizar_asistencia(estudiante.estudiante_id(df[columnas[0]][indice], current_user.id_cliente), current_user.id_cliente, id_curso, df[columnas[1]][indice], df[columnas[2]][indice], df[columnas[3]][indice], df[columnas[4]][indice], df[columnas[5]][indice], df[columnas[6]][indice], df[columnas[7]][indice], df[columnas[8]][indice], df[columnas[9]][indice], df[columnas[10]][indice], df[columnas[11]][indice], df[columnas[12]][indice], df[columnas[13]][indice], df[columnas[14]][indice], df[columnas[15]][indice], df[columnas[16]][indice], df[columnas[17]][indice], df[columnas[18]][indice], df[columnas[19]][indice], df[columnas[20]][indice], df[columnas[21]][indice], df[columnas[22]][indice], df[columnas[23]][indice], df[columnas[24]][indice], df[columnas[25]][indice], df[columnas[26]][indice], df[columnas[27]][indice], df[columnas[28]][indice], df[columnas[29]][indice], df[columnas[30]][indice]) == True:
                        flash('Se actualizo la asistencia del estudiante ' + str(df[columnas[0]][indice]))
                        pass
                    else:
                        flash('No se actualizo la asistencia del estudiante ' + str(df[columnas[0]][indice]))
                        pass
                return redirect(url_for('estudiantes.asistencia_estudiantes_id', id_curso=id_curso))
        except Exception as e:
            print(e)
            flash('No se selecciono ningun archivo, segunda condición')
            return redirect(url_for('estudiantes.asistencia_estudiantes_id', id_curso=id_curso))


@estudiantes.route('/calificaciones-estudiantes/<id_curso>/')
@login_required
def calificaciones_estudiantes_id(id_curso):
    estudiante = Estudiante()
    lista_calificaciones = estudiante.obtener_calificaciones_curso(id_curso, current_user.id_cliente)
    lista_estudiante_calificaciones=[]
    for indice in lista_calificaciones:
        # reemplazar el id del del estudiante por el nombre y el apellido y agregar el numero de documento
        estudiante_info = estudiante.obtener_estudiante(indice[2])
        lista_estudiante_calificaciones.append(estudiante_info+indice[4:15])
        
    return render_template('calificaciones.html', calificaciones=lista_estudiante_calificaciones, id_curso=id_curso)

@estudiantes.route('/calificaciones-estudiantes', methods=['POST'])
@login_required
def calificaciones_estudiantes():
    if request.method == 'POST':
        estudiante = Estudiante()
        id_curso = request.form['id_curso']
        lista_calificaciones = []
        lista_calificaciones.append(request.form.getlist('num_doc'))
        for indice in range(10):
            lista_calificaciones.append(request.form.getlist('calif_'+str(indice+1)))
        lista_calificaciones.append(request.form.getlist('observaciones'))
        for indice in range(len(lista_calificaciones[0])):
            if estudiante.actualizar_calificaciones(id_curso, estudiante.estudiante_id(lista_calificaciones[0][indice], current_user.id_cliente), current_user.id_cliente, lista_calificaciones[1][indice], lista_calificaciones[2][indice], lista_calificaciones[3][indice], lista_calificaciones[4][indice], lista_calificaciones[5][indice], lista_calificaciones[6][indice], lista_calificaciones[7][indice], lista_calificaciones[8][indice], lista_calificaciones[9][indice], lista_calificaciones[10][indice], lista_calificaciones[11][indice]) == True:
                flash('Se actualizo la calificación del estudiante ' + str(lista_calificaciones[0][indice]))
                pass
            else:
                flash('No se actualizo la calificación del estudiante ' + str(lista_calificaciones[0][indice]))
                pass
        return redirect(url_for('estudiantes.calificaciones_estudiantes_id', id_curso=id_curso))
    else:
        flash('No se actualiza la calificación del estudiantes')
        return redirect(url_for('estudiantes.calificaciones_estudiantes_id', id_curso=id_curso))

@estudiantes.route('/calificaciones-estudiantes-excel', methods=['POST'])
@login_required
def calificaciones_estudiantes_excel():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        estudiante = Estudiante()
        excel = request.files['excel']
            # verificar que el archivo sea un excel
        if not excel.filename.endswith('.xlsx'):
            flash('El archivo no es un excel')
            return redirect(url_for('estudiantes.estudiantes_curso'))
        else:
            try:
                df = pd.read_excel(excel)
                columnas = df.columns
                for indice in range(len(df[columnas[0]])):
                    if estudiante.actualizar_calificaciones(id_curso, estudiante.estudiante_id(df[columnas[0]][indice], current_user.id_cliente), current_user.id_cliente, df[columnas[1]][indice], df[columnas[2]][indice], df[columnas[3]][indice], df[columnas[4]][indice], df[columnas[5]][indice], df[columnas[6]][indice], df[columnas[7]][indice], df[columnas[8]][indice], df[columnas[9]][indice], df[columnas[10]][indice], df[columnas[11]][indice]) == True:
                        flash('Se actualizo la calificación del estudiante ' + str(df[columnas[0]][indice]))
                        pass
                    else:
                        flash('No se actualizo la calificación del estudiante ' + str(df[columnas[0]][indice]))
                        pass
                return redirect(url_for('estudiantes.calificaciones_estudiantes_id', id_curso=id_curso))
            except Exception as e:
                print(e)
                flash('No se selecciono ningun archivo')
                return redirect(url_for('estudiantes.calificaciones_estudiantes_id', id_curso=id_curso))


       

       

