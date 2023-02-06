from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, Response
# Importación de de py2pdf y reportlab

from PyPDF2 import PdfWriter, PdfReader

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import io



certificados = Blueprint('certificados', __name__, template_folder='templates', url_prefix='/')




@certificados.route('/certificados')
def certificado():
    return render_template('certificados.html')

@certificados.route('/certificados/prueba')
def certificado_post():
    certificado = crear_certificado("Juan Leonardo Ramirez Velasquez")
    # Devuelve el certificado como una respuesta HTTP
    return Response(certificado, mimetype='application/pdf')



def crear_certificado(nombre):
    packet = io.BytesIO()
    width, height = letter
    c = canvas.Canvas(packet, pagesize=(width*2, height*2))

    c.setFont("Helvetica", 13*2)
    c.drawString(340, 400, nombre)
    # centrar
    c.setFont("Helvetica", 14)
    c.drawString(360, 345, "1002527434")



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

    
    
    











  


    




