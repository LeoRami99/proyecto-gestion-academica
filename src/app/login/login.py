from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
login_page = Blueprint('login_page', __name__, template_folder='templates', url_prefix='/')

@login_page.route('/login')
def login():
  return render_template('login.html')
@login_page.route('/login_sistema', methods=['POST'])
def login_sistem():
  if request.method == 'POST':
    usuario = request.form['usuario']
    password = request.form['password']
    if usuario == 'admin' and password == 'admin':
      return redirect(url_for('login_page.login'))
    else:
      flash('Usuario o contraseña incorrectos')
      return redirect(url_for('login_page.login'))

