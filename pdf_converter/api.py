import os

from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from pdf2docx import parse
from mammoth import convert_to_html
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .inputs import DocFile

api = NinjaAPI()


def normalize_name(filename: str):
    characters = {
        '/': '\\',
        '-': '_',
        'é': 'e',
        'î': 'i'
    }
    filename = "".join(lettre for lettre in filename if lettre.isalnum())
    for key, value in characters.items():
        filename.replace(key, value)

    return filename


@api.post("/upload", description="""
                                 Télevervesement de votre fichier pdf puis conversion en word.
                                 Reçoit un fichier binaire pdf en entrée et retourne les chemins absolus
                                 des fichiers pdf et docx
                                 """)
def upload(request, file: UploadedFile = File(...)):
    pdf_file = file.read()
    # create a new instance of FileSystemStorage
    fs = FileSystemStorage()
    # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
    docx_file = file.name.split('.')[0]
    docx_file = normalize_name(docx_file)
    pdf_name = file.name[:-3]
    pdf_file = fs.save('pdf/' + normalize_name(pdf_name) + '.pdf', file)
    pdf_file_url = str(settings.BASE_DIR) + fs.url(pdf_file)
    # print(pdf_file_url, str(settings.BASE_DIR))
    docx_file = str(settings.BASE_DIR) + '/media/docs/' + normalize_name(docx_file) + '.docx'
    pdf_file_url.replace('/', '\\')
    try:
        parse(pdf_file_url, docx_file)
    except Exception:
        print("Exception")
        return {"message": "Veuillez renomez votre fichier"}
    print(docx_file, pdf_file_url)
    docx_file = docx_file.replace('/', '\\')
    return {'pdf_file': pdf_file_url, 'len': len(pdf_file), 'docx_file': docx_file}


@api.get('/convert', description="""
                                    Convertit le fichier pdf en fichier html
                                    Reçoit en entrée un json de la réponse de  l'endpoint '/upload'
                                    les chemins absolues des fichiers pdf et docx 
                                """)
def convert(request, file: DocFile):
    with open(file.docx_file, "rb") as docx_file:
        result = convert_to_html(docx_file)
        html = result.value  # The generated HTML
    os.remove(file.pdf_file)
    os.remove(file.docx_file)
    return {"html": html}

