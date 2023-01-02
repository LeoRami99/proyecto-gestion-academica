from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

cursos = Blueprint('cursos', __name__, template_folder='templates', url_prefix='/')

@cursos.route('/cursos')
@login_required
def index():
    return render_template('cursos.html')

# @cursos.route('/registrar_curso', methods=['GET', 'POST'])
# @login_required
# def registrar_curso():
#     if request.method == 'POST':
        
  
