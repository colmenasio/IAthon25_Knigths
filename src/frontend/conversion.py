import os
import requests
from docx import Document
from pptx import Presentation
from pdfdocument.document import PDFDocument
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image

# Ruta del archivo HTML
html_file = r"C:/Users/Celia/Desktop/IAthon/example.html"

# Abrir y leer el archivo HTML
with open(html_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Procesar el contenido del HTML con BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

#### CONVERSIÓN A WORD ####
# Crear un nuevo documento de Word
doc = Document()

# Agregar contenido al documento
for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
    if element.name == 'h1':
        doc.add_heading(element.text, level=1)
    elif element.name == 'h2':
        doc.add_heading(element.text, level=2)
    elif element.name == 'h3':
        doc.add_heading(element.text, level=3)
    elif element.name == 'p':
        doc.add_paragraph(element.text)

# Agregar imágenes al documento Word
for img_tag in soup.find_all('img'):
    img_url = img_tag.get('src')
    if img_url:
        try:
            img_data = requests.get(img_url).content
            img_stream = BytesIO(img_data)
            doc.add_picture(img_stream)
        except requests.exceptions.RequestException:
            print(f"Error al descargar la imagen: {img_url}")

# Guardar el archivo de Word
docx_path = 'documento.docx'
if os.path.exists(docx_path):
    os.remove(docx_path)
doc.save(docx_path)
print("Documento Word generado correctamente.")

#### CONVERSIÓN A PDF ####
# Crear un archivo PDF utilizando pdfdocument
pdf = PDFDocument('documento.pdf')
pdf.init_report()

# Agregar contenido al PDF extraído del HTML
for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
    if element.name == 'h1':
        pdf.h1(element.text)
    elif element.name == 'h2':
        pdf.h2(element.text)
    elif element.name == 'h3':
        pdf.h3(element.text)
    elif element.name == 'p':
        pdf.p(element.text)

# Agregar imágenes al PDF
for img_tag in soup.find_all('img'):
    img_url = img_tag.get('src')
    if img_url:
        try:
            img_data = requests.get(img_url).content
            img_stream = BytesIO(img_data)
            pdf.image(img_stream, width=200, height=200)  # Ajustar el tamaño si es necesario
        except requests.exceptions.RequestException:
            print(f"Error al descargar la imagen: {img_url}")

# Guardar el PDF
pdf.generate()
print("PDF generado correctamente.")

#### CONVERSIÓN A PPT ####
# Crear una presentación PowerPoint
prs = Presentation()
slide_layout = prs.slide_layouts[1]  # Diseño de diapositiva con título y contenido

# Agregar contenido a la presentación
for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.shapes.placeholders[1]

    if element.name == 'h1':
        title.text = element.text
    elif element.name == 'h2' or element.name == 'h3' or element.name == 'p':
        content.text = element.text

# Agregar imágenes a las diapositivas
for img_tag in soup.find_all('img'):
    img_url = img_tag.get('src')
    if img_url:
        try:
            img_data = requests.get(img_url).content
            img_stream = BytesIO(img_data)
            for slide in prs.slides:
                slide.shapes.add_picture(img_stream, 50, 50, width=400, height=300)  # Ajustar la posición y tamaño de la imagen
        except requests.exceptions.RequestException:
            print(f"Error al descargar la imagen: {img_url}")

# Guardar el archivo PowerPoint
ppt_path = 'documento.pptx'
if os.path.exists(ppt_path):
    os.remove(ppt_path)
prs.save(ppt_path)
print("Presentación PowerPoint generada correctamente.")
