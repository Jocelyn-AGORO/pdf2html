from django.shortcuts import render
from pdf2docx import parse
from datetime import datetime
from mammoth import convert_to_html
from django.core.files.storage import FileSystemStorage
from django.conf import settings


def conversion_page(request):
    return render(request, 'converter.html')


def convert(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        # create a new instance of FileSystemStorage
        fs = FileSystemStorage()
        # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
        pdf_file = request.FILES.get('pdf_file')
        print(pdf_file)
        docx_file = pdf_file.name + str(datetime.now()) + '.docx'
        pdf_file = fs.save('pdf/' + pdf_file.name, pdf_file)
        pdf_file_url = str(settings.BASE_DIR) + fs.url(pdf_file)
        print(pdf_file_url)
        parse(pdf_file_url, docx_file)
        # with open(docx_file, "rb") as docx_file:
        #     result = convert_to_html(docx_file)
        #     html = result.value  # The generated HTML
        return render(request, 'download.html', {"html_file": docx_file})  # , {"html_file": html}
    return render(request, 'download.html')


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


def upload(request):
    pdf_file = request.FILES['pdf_file']
    # create a new instance of FileSystemStorage
    fs = FileSystemStorage()
    # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
    docx_file = pdf_file.name.split('.')[0]
    docx_file = normalize_name(docx_file)
    pdf_name = pdf_file.name[:-3]
    pdf_file = fs.save('pdf/' + normalize_name(pdf_name)+'.pdf', pdf_file)
    pdf_file_url = str(settings.BASE_DIR) + fs.url(pdf_file)
    # print(pdf_file_url, str(settings.BASE_DIR))
    docx_file = str(settings.BASE_DIR) + '/media/docs/' + normalize_name(docx_file) + '.docx'
    pdf_file_url.replace('/', '\\')
    try:
        parse(pdf_file_url, docx_file)
    except Exception:
        print("Exception")
        return render(request, 'download.html', {"message": "Veuillez renomez votre fichier"})
    print(docx_file, pdf_file_url)
    docx_file = docx_file.replace('/', '\\')
    return render(request, 'download.html', {'name': pdf_file_url, 'docx_file': docx_file})


def conversion(request, docxfile: str):
    with open(docxfile, "rb") as docxfile:
        result = convert_to_html(docxfile)
        html = result.value  # The generated HTML
    return render(request, 'html_file.html', {"html": html})
