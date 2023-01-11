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
        if nombres and apellidos and tipo_doc and num_doc and correo and telefono and tel_fijo and ciudad:
            estudiante = Estudiante(nombres, apellidos, tipo_doc, num_doc, correo, telefono, tel_fijo, ciudad, current_user.id_cliente, "1")
            if Estudiante.verificacion_estudiantes(num_doc, current_user.id_cliente):
                flash('El estudiante ya se encuentra registrado')
                return redirect(url_for('estudiantes.registro_estudiantes'))
            else:
                if estudiante.guardar_estudiante():
                    flash('Estudiante registrado correctamente')
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
    for curso in cursos:
        if estudiantes.count_usuarios_cupo(curso[0], current_user.id_cliente) == curso[10]:
            pass
        else:
            curso_lista.append(curso)
    return render_template('estudiantesxcurso.html', cursos=curso_lista)




    return render_template('estudiantesxcurso.html', cursos=cursos)


# asignar estudiantes al curso
@estudiantes.route('/asignar-estudiantes', methods=['POST'])
@login_required
def asignar_estudiantes():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin   = request.form['fecha_fin']

        if id_curso:
            curso_indice = Curso()
            estudiantes = Estudiante()
            lista_estudiantes=[]
            # Se obtiene el cupo del curso  
            for indice in range(curso_indice.obtener_curso(id_curso)[10]):
                lista_estudiantes.append(request.form['estudiante_'+str(indice+1)])
            for indice_estudiantes in lista_estudiantes:
                # verificar que este en la base de datos de estudiantes
                print(estudiantes.estudiante_id(indice_estudiantes, current_user.id_cliente))
                if estudiantes.estudiante_id(indice_estudiantes, current_user.id_cliente) != False:
                    if estudiantes.asignar_estudiante_curso(id_curso, estudiantes.estudiante_id(indice_estudiantes, current_user.id_cliente), current_user.id_cliente, fecha_inicio, fecha_fin):
                        flash('Estudiante asignado correctamente')
                        pass
                    else:
                        flash('No se pudo asignar el estudiante')
                        pass
                else:
                    flash('El estudiante no se encuentra registrado')
                    pass
            return redirect(url_for('estudiantes.estudiantes_curso'))
        else:
            flash('Todos los campos son obligatorios')
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
