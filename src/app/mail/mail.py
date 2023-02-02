from smtplib import SMTPException
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message, Mail
mail = Mail()

def send_async_email(app, msg, nombre_estudiante, nombres_docente, nombre_curso, codigo_curso, modalidad, duracion, fecha_inicio, fecha_fin, horario, enlace_clase, enlace_grabaciones, cantidad_sesiones, ubicacion):
    with app.app_context():
        try:
            msg.html = render_template('template_corre_registro.html', nombre_estudiante=nombre_estudiante, nombres_docente=nombres_docente, 
            nombre_curso=nombre_curso, codigo_curso=codigo_curso, modalidad=modalidad, duracion=duracion, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, horario=horario, 
            enlace_clase=enlace_clase, enlace_grabaciones=enlace_grabaciones, cantidad_sesiones=cantidad_sesiones, ubicacion=ubicacion)
            mail.send(msg)
            print("Sending email to: ", msg.recipients)
            print("Sending email from: ", msg.sender)
            print("Sending email subject: ", msg.subject)
            print("Sending email body: ", msg.body)
            
        except SMTPException as e:
            print("Error al enviar correo", e)
            return e
def enviar_correo_estudiante(asunto, correo, nombre_estudiante, nombres_docente, nombre_curso, codigo_curso, modalidad, duracion, fecha_inicio, fecha_fin, horario, enlace_clase, enlace_grabaciones, cantidad_sesiones, ubicacion):
    app = current_app._get_current_object()
    msg = Message(asunto, sender=app.config['MAIL_USERNAME'], recipients=[correo])
    Thread(target=send_async_email, args=(app, msg, nombre_estudiante, nombres_docente, nombre_curso, codigo_curso, modalidad, duracion, fecha_inicio, fecha_fin, horario, enlace_clase, enlace_grabaciones, cantidad_sesiones, ubicacion)).start()
    




                
            




