from flask import Flask

from flask_login import LoginManager
# Instancias de los Blueprint
from app.login.login import login_page
from app.inicio.inicio import inicio
# from app.login.form import formulario
# from app.inicio.index import inicio
# from app.estudiante.estudiantes import estudiantes
# from app.profesor.profesor import profesor
# from app.administrador.admin import admin
# from app.jurado.jurado import jurado
# inicio de sesion
from .login.logueo import Usuario
# from .formularios.usuario import Usuario


# from app.correos.correo import correos


def createApp():
    app=Flask(__name__)
    login_manager = LoginManager()
    login_manager.login_view = 'login_page.login'
    login_manager.init_app(app)
    app.secret_key = 'mysecretkey'
    # app.config['MAIL_SERVER']='smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = 'fomalhautudecproyectos@gmail.com'
    # app.config['MAIL_PASSWORD'] = 'tcet ejwe udhe elzd'
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
    # app.register_blueprint(index)
    # app.register_blueprint(inicio)
    # app.register_blueprint(formulario)
    # app.register_blueprint(estudiantes)
    # app.register_blueprint(profesor)
    # app.register_blueprint(admin)
    # app.register_blueprint(jurado)

    return app