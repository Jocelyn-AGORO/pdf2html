from ninja import Schema


class DocFile(Schema):
    docx_file: str
    pdf_file: str

