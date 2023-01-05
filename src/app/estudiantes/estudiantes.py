from flask import Blueprint, render_template, request, redirect, url_for, flash

estudiantes = Blueprint('estudiantes', __name__, template_folder='templates', url_prefix='/')

@estudiantes.route('/estudiantes')
def index():
    return render_template('estudiantes.html')


