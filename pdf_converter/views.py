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


def upload(request):
    pdf_file = request.FILES['pdf_file']
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
    return render(request, 'download.html', {'name': pdf_file_url, 'docx_file': docx_file})


def conversion(request, docx_file_url: str):
    with open(docx_file_url, "rb") as docx_file:
        result = convert_to_html(docx_file)
        html = result.value  # The generated HTML
    return {"html": html}
