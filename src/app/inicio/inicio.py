from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

inicio = Blueprint('inicio', __name__, template_folder='templates', url_prefix='/')

@inicio.route('/inicio')
@login_required
def index():
    return render_template('inicio.html')
