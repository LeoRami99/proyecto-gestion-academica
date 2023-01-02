from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.clientes.cliente import Cliente

clientes = Blueprint('clientes', __name__, template_folder='templates', url_prefix='/clientes')

@clientes.route('/')
def index():
    return render_template('cliente.html')
@clientes.route('/registrar_cliente', methods=['GET', 'POST'])
def registrar_cliente():
    if request.method == 'POST':
      codigo = request.form['codigo_cliente']
      nombre = request.form['nombre_cliente']
      cliente = Cliente(codigo, nombre)
      if cliente.guardar_cliente():
        flash('Cliente registrado correctamente')
        return redirect(url_for('clientes.index'))
      else:
        flash('Error al registrar el cliente')
        return redirect(url_for('clientes.index'))
    

    