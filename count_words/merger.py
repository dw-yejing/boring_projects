import fitz  # PyMuPDF
import os


class Merger:
    origin_path = "out/origin.txt"

    def __init__(self, path):
        self.path = path

    def merge(self):
        if os.path.exists(self.origin_path):
            os.remove(self.origin_path)
        files = os.listdir(self.path)
        for item in files:
            self.read_pdf(os.path.join(self.path, item))

    def read_pdf(self, file_path):
        text = ""
        with fitz.open(file_path) as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()
        with open(self.origin_path, "a+", encoding="utf8") as f:
            f.write(text)
