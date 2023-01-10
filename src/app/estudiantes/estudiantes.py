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
                estudiante = Estudiante(row[columnas[0]], row[columnas[1]], row[columnas[2]], row[columnas[3]], row[columnas[4]], row[columnas[5]], row[columnas[6]], row[columnas[7]], current_user.id_cliente, "1")
                estudiante.guardar_estudiante()
            flash('Estudiantes registrados correctamente')
            return redirect(url_for('estudiantes.registro_estudiantes'))
    else:
        flash('No se pudo registrar el estudiante')
        return redirect(url_for('estudiantes.registro_estudiantes'))



       









