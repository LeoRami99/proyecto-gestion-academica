from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
#Importación de la clase Curso
from app.cursos.curso import Curso
# Clase de metodos de enviar a la base de datos
from app.estudiantes.estudiante import Estudiante
# Metodos de mail
from app.mail.mail import enviar_correo_estudiante

# Se importa pandas para leer el excel
import pandas as pd
# io 
import io
# excel 
import xlwt



estudiantes = Blueprint('estudiantes', __name__, template_folder='templates', url_prefix='/')

@estudiantes.route('/estudiantes', methods=['POST'])
# @login_required
def index():  
    estudiante = Estudiante()
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        if id_curso:
            curso = Curso().obtener_curso(id_curso)
            estudiante = estudiante.obtener_estudiantes_curso(id_curso)
            return render_template('estudiantes.html', estudiantes=estudiante, curso=curso)
    else:
        flash('No se pudo obtener los estudiantes')
        return redirect(url_for('inicio.index'))
    # return render_template('estudiantes.html')
@estudiantes.route('/eliminar-estudiante', methods=['POST'])
@login_required
def eliminar_estudiante():
    if request.method == 'POST':
        id_estudiante = request.form['id_estudiante']
        id_curso = request.form['id_curso']
        if id_estudiante and id_curso:
            estudiante = Estudiante()
            if estudiante.eliminar_estudiante_curso(id_curso, id_estudiante, current_user.id_cliente) and estudiante.eliminar_estudiante_asistencia(id_curso, id_estudiante, current_user.id_cliente) and estudiante.eliminar_estudiante_calificacion(id_curso, id_estudiante, current_user.id_cliente):
                flash('Estudiante eliminado del curso correctamente')
                return redirect(url_for('cursos.listar_cursos'))
            else:
                flash('No se pudo eliminar el estudiante')
                return redirect(url_for('cursos.listar_cursos'))
        else:
            flash('No se pudo eliminar el estudiante')
            return redirect(url_for('cursos.listar_cursos'))
    else:
        flash('No se pudo eliminar el estudiante')
        return redirect(url_for('cursos.listar_cursos'))

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
        direccion = request.form['direccion']
        sexo = request.form['sexo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        nivel_educacion = request.form['nivel_educacion']
        id_curso = request.form['id_curso']
        if nombres and apellidos and tipo_doc and num_doc and correo and telefono and tel_fijo and ciudad and direccion and sexo and fecha_nacimiento and nivel_educacion and id_curso:
            estudiante = Estudiante(nombres, apellidos, tipo_doc, num_doc, correo, telefono, tel_fijo, ciudad, current_user.id_cliente, "1", sexo  , fecha_nacimiento, nivel_educacion, direccion)
            if Estudiante.verificacion_estudiantes(num_doc, current_user.id_cliente):
                flash('El estudiante ya se encuentra registrado')
                return redirect(url_for('estudiantes.registro_estudiantes'))
            else:
                if Curso.obtener_curso_docente(id_curso) != None:
                    if estudiante.guardar_estudiante():
                        # verificar si el estudiante se registro correctamente
                        if Estudiante.verificacion_estudiantes(num_doc, current_user.id_cliente):
                            # Se obtiene el id del estudiante
                            
                            id_estudiante = Estudiante.estudiante_id(num_doc, current_user.id_cliente)
                                # Declaroación de variables para enviar el correo con los parametros correspondientes
                            nombres_docente = Curso.obtener_curso_docente(id_curso)[0] + " " + Curso.obtener_curso_docente(id_curso)[1]
                            nombre_curso = Curso.obtener_curso_docente(id_curso)[3]
                            codigo_curso = Curso.obtener_curso_docente(id_curso)[4]
                            modalidad = Curso.obtener_curso_docente(id_curso)[8]
                            duracion = Curso.obtener_curso_docente(id_curso)[9]
                            fecha_inicio = Curso.obtener_curso_docente(id_curso)[5]
                            fecha_fin = Curso.obtener_curso_docente(id_curso)[6]
                            horario = Curso.obtener_curso_docente(id_curso)[7]
                            enlace_clase = Curso.obtener_curso_docente(id_curso)[13]
                            enlace_grabaciones = Curso.obtener_curso_docente(id_curso)[14]
                            cantidad_sesiones = Curso.obtener_curso_docente(id_curso)[11]
                            ubicacion_curso = Curso.obtener_curso_docente(id_curso)[18]
                                # envio de infomación al correo
                            enviar_correo_estudiante(("Bienvenido al curso "+nombre_curso+" "+ codigo_curso), correo,nombres, nombres_docente, nombre_curso, codigo_curso, modalidad, duracion, fecha_inicio, fecha_fin, horario, enlace_clase, enlace_grabaciones, cantidad_sesiones, ubicacion_curso)
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
                    flash('Por favor asigna un docente al curso antes de registrar un estudiante')
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
            if not excel.filename.endswith('.xls'):
                flash('El archivo no es un excel')
                return redirect(url_for('estudiantes.registro_estudiantes'))
            else:
                # Se lee el excel con pandas
                df = pd.read_excel(excel)
                # Se obtiene el nombre de las columnas
                columnas = df.columns
                
                print(df)
                # Recorreror las columnas y enviar la información
                for index, row in df.iterrows():
                    # se verifica que se halla asignado un docente al curso
                    """ 
                    row[0] tipo de documento
                    row[1] número de documento
                    row[2] apellidos
                    row[3] nombres
                    row[4] fecha de nacimiento
                    row[5] sexo
                    row[6] nivel educativo
                    row[7] telefono
                    row[8] correo
                    row[9] ciudad
                    row[10] dirección
                    row[11] asesor quien hace las matriculas
                    
                    """

                    if Curso().obtener_curso_docente(id_curso) != None:
                        #Verificar que el estudiante no se encuentre previamente registrado y omitir el la columna
                        if Estudiante().verificacion_estudiantes(int(row[columnas[1]]), current_user.id_cliente) == False:
                            estudiante = Estudiante(nombres=row[columnas[3]], apellidos=row[columnas[2]], tipo_doc=row[columnas[0]], num_doc=int(row[columnas[1]]), correo=row[columnas[8]], telefono=int(row[columnas[7]]), tel_fijo=int(0), ciudad=row[columnas[9]], id_ciente=current_user.id_cliente, estado="1", sexo=row[columnas[5]], fecha_nacimiento=row[columnas[4]], nivel_educativo=row[columnas[6]], direccion=row[columnas[10]])
                            if estudiante.guardar_estudiante():
                                # verificar si el estudiante se registro correctamente
                                if Estudiante.verificacion_estudiantes(int(row[columnas[1]]), current_user.id_cliente):
                                    
                                    # objeto de bloque para la insercción de de asesor a la base de datos
                                    asesor = estudiante.insertar_asesor(id_curso, current_user.id_cliente, Estudiante.estudiante_id(int(row[columnas[1]]), current_user.id_cliente), row[columnas[11]])
                                    # Se obtiene el id del estudiante
                                    id_estudiante = Estudiante.estudiante_id(int(row[columnas[1]]), current_user.id_cliente)
                                    nombres_docente = Curso.obtener_curso_docente(id_curso)[0] + " " + Curso.obtener_curso_docente(id_curso)[1]
                                    nombre_curso = Curso.obtener_curso_docente(id_curso)[3]
                                    codigo_curso = Curso.obtener_curso_docente(id_curso)[4]
                                    modalidad = Curso.obtener_curso_docente(id_curso)[8]
                                    duracion = Curso.obtener_curso_docente(id_curso)[9]
                                    fecha_inicio = Curso.obtener_curso_docente(id_curso)[5]
                                    fecha_fin = Curso.obtener_curso_docente(id_curso)[6]
                                    horario = Curso.obtener_curso_docente(id_curso)[7]
                                    enlace_clase = Curso.obtener_curso_docente(id_curso)[13]
                                    enlace_grabaciones = Curso.obtener_curso_docente(id_curso)[14]
                                    cantidad_sesiones = Curso.obtener_curso_docente(id_curso)[11]
                                    ubicacion_curso = Curso.obtener_curso_docente(id_curso)[18]
                                    # Se envia el correo al estudiante

                                    # lista de estudiantes ya registrados
                                    

                                    # enviar_correo_estudiante(("Bienvenido al curso "+nombre_curso+" "+ codigo_curso), row[columnas[8]], row[columnas[3]], nombres_docente, nombre_curso, codigo_curso, modalidad, duracion, fecha_inicio, fecha_fin, horario, enlace_clase, enlace_grabaciones, cantidad_sesiones, ubicacion_curso)

                                    # Se registra el estudiante en el curso
                                    if Estudiante.asignar_estudiante_curso(id_curso, id_estudiante, current_user.id_cliente, datetime.now(), datetime.now()):
                                        if Estudiante.generar_info_asistencia(id_estudiante, id_curso, current_user.id_cliente) and Estudiante.generar_info_calificaciones(id_estudiante, id_curso, current_user.id_cliente):
                                            pass
                                        else:
                                            flash("Ocurrio un error al registrar el estudiante")
                                            return redirect(url_for('estudiantes.registro_estudiantes'))
                                    else:
                                        flash(str(int(row[columnas[1]])))
                                        return redirect(url_for('estudiantes.registro_estudiantes'))

                                flash('El estudiante ' + str(int(row[columnas[1]])) + ' se registro correctamente')
                                pass
                            else:
                                flash('No se pudo registrar el estudiante'+ row[columnas[1]])
                                pass
                        else:
                            # Agregar el estudiante a una lista para posteriormente descargar un txt
                            flash('Ya se encuentra registrado ' + str(int(row[columnas[1]])))
                            pass
                    else:
                        flash('Por favor asigne un docente al curso antes de registrar estudiantes')
                        return redirect(url_for('estudiantes.registro_estudiantes'))
                return redirect(url_for('estudiantes.registro_estudiantes'))
        except Exception as e:
            print("El error es aquí",e)
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
                    if estudiantes.verificar_asignacion_curso(id_curso, id_estudiante, current_user.id_cliente)==False:
                        if Curso.obtener_curso_docente(id_curso)!= None:
                            if estudiantes.asignar_estudiante_curso(id_curso, id_estudiante, current_user.id_cliente, fecha_inicio, fecha_fin):
                                estudiantes.generar_info_asistencia(id_estudiante, id_curso, current_user.id_cliente)
                                estudiantes.generar_info_calificaciones(id_estudiante, id_curso, current_user.id_cliente)

                                # Variables para enviar el correo
                                nombres_docente = Curso.obtener_curso_docente(id_curso)[0] + " " + Curso.obtener_curso_docente(id_curso)[1]
                                nombre_curso = Curso.obtener_curso_docente(id_curso)[3]
                                codigo_curso = Curso.obtener_curso_docente(id_curso)[4]
                                modalidad = Curso.obtener_curso_docente(id_curso)[8]
                                duracion = Curso.obtener_curso_docente(id_curso)[9]
                                fecha_inicio = Curso.obtener_curso_docente(id_curso)[5]
                                fecha_fin = Curso.obtener_curso_docente(id_curso)[6]
                                horario = Curso.obtener_curso_docente(id_curso)[7]
                                enlace_clase = Curso.obtener_curso_docente(id_curso)[13]
                                enlace_grabaciones = Curso.obtener_curso_docente(id_curso)[14]
                                cantidad_sesiones = Curso.obtener_curso_docente(id_curso)[11]
                                nombre_estudiante = estudiantes.obtener_estudiante(id_estudiante)[0]
                                correo = estudiantes.obtener_estudiante(id_estudiante)[3]
                                ubicacion_curso = Curso.obtener_curso_docente(id_curso)[18]

                                # enviar_correo_estudiante(("Bienvenido al curso "+nombre_curso+" "+ codigo_curso), correo, nombre_estudiante, nombres_docente, nombre_curso, codigo_curso, modalidad, duracion, fecha_inicio, fecha_fin, horario, enlace_clase, enlace_grabaciones, cantidad_sesiones, ubicacion_curso)


                                flash('El estudiante se asigno correctamente')
                                return redirect(url_for('estudiantes.estudiantes_curso'))
                            else:
                                flash('No se pudo asignar el estudiante')
                                return redirect(url_for('estudiantes.estudiantes_curso'))
                        else:
                            flash('Por favor asigna un docente al curso antes de asignar estudiantes')
                            return redirect(url_for('estudiantes.estudiantes_curso'))
                    else:
                        flash('El estudiante ya se encuentra asignado al curso')
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
                # print("Número de filas", numero_de_filas.values[0])
                # if numero_de_filas.values[0] == curso_indice.obtener_curso(id_curso)[10]:
                    # Recorreror las columnas y enviar la información
                for index, row in df.iterrows():
                        #Verificar que el estudiante no se encuentre previamente registrado y omitir el la columna
                        estudiante = Estudiante()
                        if estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente) != False:
                            # Hacer validación si el estudiante ya se encuentra asignado al curso y omitir el registro
                            if Estudiante().verificar_asignacion_curso(id_curso, estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente), current_user.id_cliente) == False:
                                if Curso.obtener_curso_docente(id_curso) != None:
                                    if estudiante.asignar_estudiante_curso(id_curso, estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente), current_user.id_cliente, fecha_inicio, fecha_fin) and estudiante.generar_info_asistencia(estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente), id_curso, current_user.id_cliente) and estudiante.generar_info_calificaciones(estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente), id_curso, current_user.id_cliente):
                                            # Variables para enviar el correo
                                        id_estudiante = estudiante.estudiante_id(row[columnas[0]], current_user.id_cliente)
                                        nombres_docente = Curso.obtener_curso_docente(id_curso)[0] + " " + Curso.obtener_curso_docente(id_curso)[1]
                                        nombre_curso = Curso.obtener_curso_docente(id_curso)[3]
                                        codigo_curso = Curso.obtener_curso_docente(id_curso)[4]
                                        modalidad = Curso.obtener_curso_docente(id_curso)[8]
                                        duracion = Curso.obtener_curso_docente(id_curso)[9]
                                        fecha_inicio = Curso.obtener_curso_docente(id_curso)[5]
                                        fecha_fin = Curso.obtener_curso_docente(id_curso)[6]
                                        horario = Curso.obtener_curso_docente(id_curso)[7]
                                        enlace_clase = Curso.obtener_curso_docente(id_curso)[13]
                                        enlace_grabaciones = Curso.obtener_curso_docente(id_curso)[14]
                                        cantidad_sesiones = Curso.obtener_curso_docente(id_curso)[11]
                                        nombre_estudiante = estudiante.obtener_estudiante(id_estudiante)[0]
                                        correo = estudiante.obtener_estudiante(id_estudiante)[3]
                                        ubicacion_curso = Curso.obtener_curso_docente(id_curso)[18]

                                        # enviar_correo_estudiante(("Bienvenido al curso "+nombre_curso+" "+ codigo_curso), correo, nombre_estudiante, nombres_docente, nombre_curso, codigo_curso, modalidad, duracion, fecha_inicio, fecha_fin, horario, enlace_clase, enlace_grabaciones, cantidad_sesiones, ubicacion_curso)
                                        flash('El estudiante ' + str(row[columnas[0]]) + ' se asigno correctamente ')
                                        pass
                                    else:
                                        pass
                                else:
                                    flash('Por favor asigna un docente al curso antes de registrar a los estudiantes.')
                                    pass
                            else:
                                flash('El estudiante ' + str(row[columnas[0]]) + ' ya se encuentra registrado en el curso')
                                pass
                        else:
                            flash('El estudiante ' + str(row[columnas[0]]) + ' no se encuentra registrado')
                            pass
                return redirect(url_for('estudiantes.estudiantes_curso'))
                # else:
                #     flash('El número de estudiantes en el excel no coincide con el cupo del curso')
                #     return redirect(url_for('estudiantes.estudiantes_curso'))
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
    if current_user.rol == "AD" or current_user.rol == "ADV":
        for indice in curso.obtener_cursos(current_user.id_cliente):
            if indice[14]==1:
                lista_cursos_activos.append(indice)
            else:
                pass
    elif current_user.rol == "DOC":
        # mostrar los cursos que tiene asignado el docente
        for indice in asig_doc:
           for indice2 in cursos:
               if indice[1] == indice2[0]:
                   if indice2[14]==1:
                       lista_cursos_activos.append(indice2)
                   else:
                       pass
               else:
                   pass
    return render_template('asistencia_calificacion.html', cursos=lista_cursos_activos)
    # return render_template('asistencia_calificacion.html', cursos=lista_cursos_activos)
@estudiantes.route('/asistencia-estudiantes', methods=['GET', 'POST'])
@login_required
def asistencia_estudiantes_id():
    id_curso = request.args.get('id_curso')
    if Curso().obtener_estado_curso(id_curso) > 0:
        # Este parametro de curso contiene la cantidad de horas de asistencias
        parametro_curso = Curso().obtener_reg_curso_id(Curso.obtener_curso(id_curso)[17])[6]
        estudiante = Estudiante()
        lista_asistencia = estudiante.obtener_asistencia_curso(id_curso, current_user.id_cliente)
        lista_estudiante_asistencia=[]
        for indice in lista_asistencia:
            # reemplazar el id del del estudiante por el nombre y el apellido y agregar el numero de documento
            estudiante_info = estudiante.obtener_estudiante(indice[1])
            # print("id del estudiante",indice[0])
            lista_estudiante_asistencia.append(estudiante_info + indice[4:35]) 
        return render_template('asistencia.html', asistencia=lista_estudiante_asistencia, id_curso=id_curso, parametro_curso=parametro_curso)
    else:
        flash('No se puede ingresar a las asistencias del curso, el curso está finalizado o no existe')
        return redirect(url_for('estudiantes.asistencia_estudiantes'))

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
        lista_asistencias.append(request.form.getlist('observaciones'))
        estudiante = Estudiante()
        print(lista_asistencias)
        # print(lista_asistencias[0])
        for indice in range(len(lista_asistencias[0])):
            

            # Condifición con 33 datos para el envio de información
            if estudiante.actualizar_asistencia(estudiante.estudiante_id(lista_asistencias[0][indice], current_user.id_cliente), current_user.id_cliente, id_curso, lista_asistencias[1][indice], lista_asistencias[2][indice], lista_asistencias[3][indice], lista_asistencias[4][indice], lista_asistencias[5][indice], lista_asistencias[6][indice], lista_asistencias[7][indice], lista_asistencias[8][indice], lista_asistencias[9][indice], lista_asistencias[10][indice], lista_asistencias[11][indice], lista_asistencias[12][indice], lista_asistencias[13][indice], lista_asistencias[14][indice], lista_asistencias[15][indice], lista_asistencias[16][indice], lista_asistencias[17][indice], lista_asistencias[18][indice], lista_asistencias[19][indice], lista_asistencias[20][indice], lista_asistencias[21][indice], lista_asistencias[22][indice], lista_asistencias[23][indice], lista_asistencias[24][indice], lista_asistencias[25][indice], lista_asistencias[26][indice], lista_asistencias[27][indice], lista_asistencias[28][indice], lista_asistencias[29][indice], lista_asistencias[30][indice], lista_asistencias[31][indice])==True:
                # print((lista_asistencias[0][indice], current_user.id_cliente), id_curso, current_user.id_cliente, lista_asistencias[1][indice], lista_asistencias[2][indice], lista_asistencias[3][indice], lista_asistencias[4][indice], lista_asistencias[5][indice], lista_asistencias[6][indice], lista_asistencias[7][indice], lista_asistencias[8][indice], lista_asistencias[9][indice], lista_asistencias[10][indice], lista_asistencias[11][indice], lista_asistencias[12][indice], lista_asistencias[13][indice], lista_asistencias[14][indice], lista_asistencias[15][indice], lista_asistencias[16][indice], lista_asistencias[17][indice], lista_asistencias[18][indice], lista_asistencias[19][indice], lista_asistencias[20][indice], lista_asistencias[21][indice], lista_asistencias[22][indice], lista_asistencias[23][indice], lista_asistencias[24][indice], lista_asistencias[25][indice], lista_asistencias[26][indice], lista_asistencias[27][indice], lista_asistencias[28][indice], lista_asistencias[29][indice], lista_asistencias[30][indice])
                flash('Se actualizo la asistencia del estudiante ' + str(lista_asistencias[0][indice]))
                pass
            else:
                flash('No se actualizo la asistencia del estudiante ' + str(lista_asistencias[0][indice]))
                pass
        return redirect(url_for('estudiantes.asistencia_estudiantes_id', id_curso=id_curso))
    else:
        flash('No se actualiza la asistencia')
        return redirect(url_for('estudiantes.asistencia_estudiantes', id_curso=id_curso))
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


@estudiantes.route('/calificaciones-estudiantes/', methods=['GET'])
@login_required
def calificaciones_estudiantes_id():
    id_curso = request.args.get('id_curso')
    # este parametro de curso es para las calificaciones
    try:
        parametro_curso = Curso().obtener_reg_curso_id(Curso.obtener_curso(id_curso)[17])[4]
        if parametro_curso != None:
            if Curso().obtener_estado_curso(id_curso) > 0:
                estudiante = Estudiante()
                lista_calificaciones = estudiante.obtener_calificaciones_curso_id(id_curso, current_user.id_cliente)
                lista_estudiante_calificaciones=[]
                for indice in lista_calificaciones:
                    estudiante_info = estudiante.obtener_estudiante(indice[0])
                    # agregar calif_10 que es la ultima calificacion
                    nota_final = indice[-1]
                    lista_estudiante_calificaciones.append(estudiante_info+indice[:parametro_curso+1]+(nota_final,))



                    # reemplazar el id del del estudiante por el nombre y el apellido y agregar el numero de documento
                    # estudiante_info = estudiante.obtener_estudiante(indice[2])
                    # # lista_estudiante_calificaciones.append(estudiante_info+indice[parametro_curso])
                    # lista_estudiante_calificaciones = [estudiante_info + indice[4:parametro_curso+5] for indice in lista_calificaciones]
                return render_template('calificaciones.html', calificaciones=lista_estudiante_calificaciones, id_curso=id_curso, parametro_curso=parametro_curso)
            else:
                flash('No se puede ingresar a las calificaciones del curso, el curso no esta activo')
                return redirect(url_for('estudiantes.asistencia_estudiantes'))
    except Exception as e:
        flash('No se puede ingresar a las calificaciones del curso, el curso no esta activo')
        return redirect(url_for('estudiantes.asistencia_estudiantes'))

@estudiantes.route('/calificaciones-estudiantes', methods=['POST'])
@login_required
def calificaciones_estudiantes():
    if request.method == 'POST':
        estudiante = Estudiante()
        id_curso = request.form['id_curso']
        lista_calificaciones = []
        lista_calificaciones.append(request.form.getlist('num_doc'))
        parametro_nota= Curso().obtener_reg_curso_id(Curso.obtener_curso(id_curso)[17])[4]
        print("este es el parametro de la nota:", parametro_nota)
        suma_nota = 0
        nota_final = 0
        
        for indice in range(10):
            lista_calificaciones.append(request.form.getlist('calif_'+str(indice+1)))
        lista_calificaciones.append(request.form.getlist('observaciones'))
        for indice in range(len(lista_calificaciones[0])):
            suma_nota = float(lista_calificaciones[1][indice])+float(lista_calificaciones[2][indice])+float(lista_calificaciones[3][indice])+float(lista_calificaciones[4][indice])+float(lista_calificaciones[5][indice])+float(lista_calificaciones[6][indice])+float(lista_calificaciones[7][indice])+float(lista_calificaciones[8][indice])+float(lista_calificaciones[9][indice])
            nota_final = round(suma_nota/parametro_nota, 2)
            if estudiante.actualizar_calificaciones(id_curso, estudiante.estudiante_id(lista_calificaciones[0][indice], current_user.id_cliente), current_user.id_cliente, lista_calificaciones[1][indice], lista_calificaciones[2][indice], lista_calificaciones[3][indice], lista_calificaciones[4][indice], lista_calificaciones[5][indice], lista_calificaciones[6][indice], lista_calificaciones[7][indice], lista_calificaciones[8][indice], lista_calificaciones[9][indice], nota_final, lista_calificaciones[11][indice]) == True:
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
            return redirect(url_for('estudiantes.calificaciones_estudiantes_id', id_curso=id_curso))
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

"""
    Descargar asistencias y calificaciones por curso en excel
"""
@estudiantes.route('/descargar-asistencias', methods=['POST'])
@login_required
def descargar_asistencias():
    if request.method == 'POST':
        try:
            id_curso = request.form['id_curso']
            estudiante = Estudiante()
            lista_asistencia = estudiante.obtener_asistencia(id_curso)
            # Guardar en un excel las asistencias
            salida = io.BytesIO()
            libro = xlwt.Workbook()
            hoja = libro.add_sheet('Asistencias')
            hoja.write(0, 0, 'Apellido')
            hoja.write(0, 1, 'Nombre')
            hoja.write(0, 2, 'Número de identificación')
            hoja.write(0, 3, 'Asistencia 1')
            hoja.write(0, 4, 'Asistencia 2')
            hoja.write(0, 5, 'Asistencia 3')
            hoja.write(0, 6, 'Asistencia 4')
            hoja.write(0, 7, 'Asistencia 5')
            hoja.write(0, 8, 'Asistencia 6')
            hoja.write(0, 9, 'Asistencia 7')
            hoja.write(0, 10, 'Asistencia 8')
            hoja.write(0, 11, 'Asistencia 9')
            hoja.write(0, 12, 'Asistencia 10')
            hoja.write(0, 13, 'Asistencia 11')
            hoja.write(0, 14, 'Asistencia 12')
            hoja.write(0, 15, 'Asistencia 13')
            hoja.write(0, 16, 'Asistencia 14')
            hoja.write(0, 17, 'Asistencia 15')
            hoja.write(0, 18, 'Asistencia 16')
            hoja.write(0, 19, 'Asistencia 17')
            hoja.write(0, 20, 'Asistencia 18')
            hoja.write(0, 21, 'Asistencia 19')
            hoja.write(0, 22, 'Asistencia 20')
            hoja.write(0, 23, 'Asistencia 21')
            hoja.write(0, 24, 'Asistencia 22')
            hoja.write(0, 25, 'Asistencia 23')
            hoja.write(0, 26, 'Asistencia 24')
            hoja.write(0, 27, 'Asistencia 25')
            hoja.write(0, 28, 'Asistencia 26')
            hoja.write(0, 29, 'Asistencia 27')
            hoja.write(0, 30, 'Asistencia 28')
            hoja.write(0, 31, 'Asistencia 29')
            hoja.write(0, 32, 'Asistencia 30')
                

            for indice in range(len(lista_asistencia)):
                hoja.write(indice+1, 0, lista_asistencia[indice][2])
                hoja.write(indice+1, 1, lista_asistencia[indice][1])
                hoja.write(indice+1, 2, lista_asistencia[indice][0])
                hoja.write(indice+1, 3, int(lista_asistencia[indice][3]))
                hoja.write(indice+1, 4, int(lista_asistencia[indice][4]))
                hoja.write(indice+1, 5, int(lista_asistencia[indice][5]))
                hoja.write(indice+1, 6, int(lista_asistencia[indice][6]))
                hoja.write(indice+1, 7, int(lista_asistencia[indice][7]))
                hoja.write(indice+1, 8, int(lista_asistencia[indice][8]))
                hoja.write(indice+1, 9, int(lista_asistencia[indice][9]))
                hoja.write(indice+1, 10, int(lista_asistencia[indice][10]))
                hoja.write(indice+1, 11, int(lista_asistencia[indice][11]))
                hoja.write(indice+1, 12, int(lista_asistencia[indice][12]))
                hoja.write(indice+1, 13, int(lista_asistencia[indice][13]))
                hoja.write(indice+1, 14, int(lista_asistencia[indice][14]))
                hoja.write(indice+1, 15, int(lista_asistencia[indice][15]))
                hoja.write(indice+1, 16, int(lista_asistencia[indice][16]))
                hoja.write(indice+1, 17, int(lista_asistencia[indice][17]))
                hoja.write(indice+1, 18, int(lista_asistencia[indice][18]))
                hoja.write(indice+1, 19, int(lista_asistencia[indice][19]))
                hoja.write(indice+1, 20, int(lista_asistencia[indice][20]))
                hoja.write(indice+1, 21, int(lista_asistencia[indice][21]))
                hoja.write(indice+1, 22, int(lista_asistencia[indice][22]))
                hoja.write(indice+1, 23, int(lista_asistencia[indice][23]))
                hoja.write(indice+1, 24, int(lista_asistencia[indice][24]))
                hoja.write(indice+1, 25, int(lista_asistencia[indice][25]))
                hoja.write(indice+1, 26, int(lista_asistencia[indice][26]))
                hoja.write(indice+1, 27, int(lista_asistencia[indice][27]))
                hoja.write(indice+1, 28, int(lista_asistencia[indice][28]))
                hoja.write(indice+1, 29, int(lista_asistencia[indice][29]))
                hoja.write(indice+1, 30, int(lista_asistencia[indice][30]))
                hoja.write(indice+1, 31, int(lista_asistencia[indice][31]))
                hoja.write(indice+1, 32, int(lista_asistencia[indice][32]))
            libro.save(salida)
            salida.seek(0)
            return Response(salida, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=asistencias.xls"})
        except Exception as e:
            flash("Error al generar el archivo excel")
            return redirect(url_for('estudiantes.asistencia_estudiantes'))
@estudiantes.route('/descargar-calificaciones', methods=['POST'])
@login_required
def descargar_calificaciones():
    if request.method == 'POST':
        try:
            id_curso = request.form['id_curso']
            salida = io.BytesIO()
            libro = xlwt.Workbook()
            hoja = libro.add_sheet('Calificaciones')
            lista_calificaciones = Estudiante().obtener_calificacion(id_curso)
            hoja.write(0, 0, 'Apellido')
            hoja.write(0, 1, 'Nombre')
            hoja.write(0, 2, 'Número de identificación')
            hoja.write(0, 3, 'Calificacion 1')
            hoja.write(0, 4, 'Calificacion 2')
            hoja.write(0, 5, 'Calificacion 3')
            hoja.write(0, 6, 'Calificacion 4')
            hoja.write(0, 7, 'Calificacion 5')
            hoja.write(0, 8, 'Calificacion 6')
            hoja.write(0, 9, 'Calificacion 7')
            hoja.write(0, 10, 'Calificacion 8')
            hoja.write(0, 11, 'Calificacion 9')
            hoja.write(0, 12, 'Calificación final')
            hoja.write(0, 13, 'Observaciones')

            for indice in range(len(lista_calificaciones)):
                hoja.write(indice+1, 0, lista_calificaciones[indice][2])
                hoja.write(indice+1, 1, lista_calificaciones[indice][1])
                hoja.write(indice+1, 2, lista_calificaciones[indice][0])
                hoja.write(indice+1, 3, float(lista_calificaciones[indice][3]))
                hoja.write(indice+1, 4, float(lista_calificaciones[indice][4]))
                hoja.write(indice+1, 5, float(lista_calificaciones[indice][5]))
                hoja.write(indice+1, 6, float(lista_calificaciones[indice][6]))
                hoja.write(indice+1, 7, float(lista_calificaciones[indice][7]))
                hoja.write(indice+1, 8, float(lista_calificaciones[indice][8]))
                hoja.write(indice+1, 9, float(lista_calificaciones[indice][9]))
                hoja.write(indice+1, 10, float(lista_calificaciones[indice][10]))
                hoja.write(indice+1, 11, float(lista_calificaciones[indice][11]))
                hoja.write(indice+1, 12, float(lista_calificaciones[indice][12]))
                hoja.write(indice+1, 13, lista_calificaciones[indice][13])

            libro.save(salida)
            salida.seek(0)
            return Response(salida, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=calificaciones.xls"})
        except Exception as e:
            flash("Error al generar el archivo excel")
            return redirect(url_for('estudiantes.calificaciones_estudiantes'))


""" 
Se crea un petición para descargar la información de los asesores en un archio excel

 """
@estudiantes.route('/descargar-asesores', methods=['POST'])
def descarga_asesores():
    asesores = Estudiante().obtener_info_asesores(current_user.id_cliente)
    if asesores is False or None:
        flash("No hay asesores registrados")
        return redirect(url_for('estudiantes.asesores_estudiantes'))
    else:
        # Archivo excel que se va a descargar
        salida = io.BytesIO()
        # Se crea el libro de excel
        libro = xlwt.Workbook()
        # Se crea la hoja de excel
        hoja = libro.add_sheet('Asesores')
        
        #aplicar estilos a los encabezados y colocar color de fondo y bordes

        estilo = xlwt.easyxf('font: bold 1, color black; pattern: pattern solid, fore_colour gray25; align: horiz center; borders: left thin, right thin, top thin, bottom thin')
        estilo_bordes = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin')
        

        
        
        # Se escriben los encabezados de la hoja de excel
        hoja.write(0, 0, 'Nombre', estilo)
        hoja.write(0, 1, 'Apellido', estilo)
        hoja.write(0, 2, 'Número de identificación', estilo)
        hoja.write(0, 3, 'Nombre del curso', estilo)
        hoja.write(0, 4, 'Código del curso', estilo)
        hoja.write(0, 5, 'Nombre del asesor', estilo)

        # Se recorre la lista de asesores para escribirlos en la hoja de excel
        for indice in range(len(asesores)):
            hoja.write(indice+1, 0, asesores[indice][0], estilo_bordes)
            hoja.write(indice+1, 1, asesores[indice][1], estilo_bordes)
            hoja.write(indice+1, 2, asesores[indice][2], estilo_bordes)
            hoja.write(indice+1, 3, asesores[indice][3], estilo_bordes)
            hoja.write(indice+1, 4, asesores[indice][4], estilo_bordes)
            hoja.write(indice+1, 5, asesores[indice][5], estilo_bordes)

        # Se guarda el archivo excel
        libro.save(salida)
        # Se retorna el archivo excel
        salida.seek(0)
        return Response(salida, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=asesores.xls"})

