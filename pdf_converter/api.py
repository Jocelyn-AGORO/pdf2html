from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from pdf2docx import parse
from datetime import datetime
from mammoth import convert_to_html
from django.core.files.storage import FileSystemStorage
from django.conf import settings

api = NinjaAPI()


@api.post("/upload", url_name='upload')
def upload(request, file: UploadedFile = File(...)):
    pdf_file = file.read()
    # create a new instance of FileSystemStorage
    fs = FileSystemStorage()
    # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
    print(pdf_file)
    docx_file = pdf_file.name + str(datetime.now()) + '.docx'
    pdf_file = fs.save('pdf/' + pdf_file.name, pdf_file)
    pdf_file_url = str(settings.BASE_DIR) + fs.url(pdf_file)
    print(pdf_file)
    docx_file = pdf_file_url + '.docx'
    parse(pdf_file_url, docx_file)
    return {'name': pdf_file_url, 'len': len(pdf_file), 'docx_file_url': docx_file}


@api.get('/convert')
def convert(request, docx_file_url: str):
    with open(docx_file_url, "rb") as docx_file:
        result = convert_to_html(docx_file)
        html = result.value  # The generated HTML
    return {"html": html}
