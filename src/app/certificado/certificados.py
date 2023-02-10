from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, Response
# Importación de de py2pdf y reportlab

from PyPDF2 import PdfWriter, PdfReader

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import io
import qrcode

# Clase para la consulta de resultados
from app.certificado.certificado import Certificado 


certificados = Blueprint('certificados', __name__, template_folder='templates', url_prefix='/')




@certificados.route('/certificados')
def certificado():
    return render_template('certificado.html')


@certificados.route('/certificados/generar', methods=['POST'])
def certificado_generar():
    codigo_curso = request.form['codigo_curso']
    num_doc = request.form['num_doc']

    if codigo_curso and num_doc:
        curso = Certificado().obtener_info_curso(codigo_curso)
        if curso:
            nombre = Certificado().obtener_nombre(num_doc)
            if nombre:
                certificado = crear_certificado(nombre)
                # Devuelve el certificado como una respuesta HTTP
                return Response(certificado, mimetype='application/pdf')
            else:
                flash('El número de documento no existe')
                return redirect(url_for('certificados.certificado'))

    





@certificados.route('/certificados/prueba')
def certificado_post():
    certificado = crear_certificado("JUAN LEONARDO RAMIREZ VELASQUEZ")
    # Devuelve el certificado como una respuesta HTTP
    return Response(certificado, mimetype='application/pdf')



def crear_certificado(nombre):
    packet = io.BytesIO()
    width, height = letter
    print("estan son las medidas del pdf", width, height)
    c = canvas.Canvas(packet, pagesize=(width*2, height*2))
    font = TTFont('Hurme', 'HurmeGeometricSans4.ttf')

    pdfmetrics.registerFont(font)
    # Nombres y apellidos
    c.setFont("Hurme", 20)
    c.drawCentredString(400, 400, nombre)
    # Número de documento
    c.setFont("Hurme", 20)
    c.drawCentredString(410, 343, "1002527434")
    # Curso
    c.setFont("Hurme", 26)
    # color de la fuente
    c.setFillColor("#0067B1")
    c.drawCentredString(400, 280, "Analítica De Datos Y Big Data".upper())
    # Crea un código QR
    data_qr = "http://192.168.1.53:5000/inicio"  
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(data_qr)
    qr.make(fit=True)
    # Se dibuja el código QR en el PDF
    c.drawInlineImage(qr.make_image().get_image(), 50, 50, width=100, height=100)


    # Guarda el PDF
    c.save()

    plantilla = PdfReader(open("plantilla.pdf", "rb"))
    page = plantilla.pages[0]

    packet.seek(0)

    nuevo_pdf = PdfReader(packet)
    page.merge_page(nuevo_pdf.pages[0])

    writer = PdfWriter()
    writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    return output.read()




    
    
    











  


    




