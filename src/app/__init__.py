from flask import Flask, render_template

from flask_login import LoginManager
# Instancias de los Blueprint
from app.login.login import login_page
from app.inicio.inicio import inicio
from app.cursos.cursos import cursos
from app.clientes.clientes import clientes
from app.estudiantes.estudiantes import estudiantes
from app.docentes.docentes import docentes

# inicio de sesion
from .login.logueo import Usuario
# from .formularios.usuario import Usuario


# from app.correos.correo import correos


def createApp():
    app=Flask(__name__)
    # Manejo de errores
    app.register_error_handler(404, lambda e: render_template('404.html'))

    # Manejo de usuario
    login_manager = LoginManager()
    login_manager.login_view = 'login_page.login'
    login_manager.init_app(app)
    app.secret_key = 'mysecretkey'
    # app.config['MAIL_SERVER']='smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = 'correos@gmail.com'
    # app.config['MAIL_PASSWORD'] = ''
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = True
    # mail = Mail()
    # mail.init_app(app)
    
    @login_manager.user_loader
    def load_user(nombre_usuario):
        return Usuario.obtener_usuario(nombre_usuario)


    # Registro de los Blueprint
    app.register_blueprint(login_page)
    app.register_blueprint(inicio)
    app.register_blueprint(cursos)
    app.register_blueprint(clientes)
    app.register_blueprint(estudiantes)
    app.register_blueprint(docentes)

    return app