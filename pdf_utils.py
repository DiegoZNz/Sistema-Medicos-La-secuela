from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter

def generar_pdf_receta(nombre_paciente, texto_receta, url_imagen_centro):
    # Crear un objeto PDF y establecer el tamaño del documento
    doc = SimpleDocTemplate("receta.pdf", pagesize=letter)

    # Crear una lista para almacenar los elementos del contenido del PDF
    content = []

    # Agregar el nombre del paciente y el espacio para el texto de la receta
    styles = getSampleStyleSheet()
    content.append(Spacer(1, 30))
    content.append(Paragraph(f"Nombre del paciente: {nombre_paciente}", styles['Normal']))
    content.append(Spacer(1, 20))
    content.append(Paragraph("Receta:", styles['Normal']))
    content.append(Paragraph(texto_receta, styles['Normal']))

    # Construir el PDF sin la imagen
    doc.build(content)

    # Crear un objeto Canvas para agregar la imagen al PDF generado
    from reportlab.pdfgen import canvas
    c = canvas.Canvas("receta.pdf", pagesize=letter)
    # Agregar la imagen del centro médico en la esquina superior izquierda del PDF
    image = Image(url_imagen_centro, width=150, height=50)
    image.drawOn(c, 40, 750)  # Ajustar las coordenadas según tu preferencia

    # Guardar los cambios y cerrar el objeto Canvas
    c.save()
