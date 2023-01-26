from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint

certificados = Blueprint('certificados', __name__, template_folder='templates', url_prefix='/')

@certificados.route('/certificados')
def certificados():
    return render_template('certificados.html')