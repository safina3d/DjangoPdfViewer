from django.db import models
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError


class FichierPdf(models.Model):
    """
    Pdf File Model
    """
    pdf_file = models.FileField(upload_to='pdf_docs')
    nb_pages = models.IntegerField(default=0)

    def __str__(self):
        return "File: {} >>>> NbPages: {}".format(self.pdf_file, self.nb_pages)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.nb_pages = FichierPdf.get_nb_page(self.pdf_file)
        super(FichierPdf, self).save(force_insert, force_update)

    @staticmethod
    def get_nb_page(pdf_file):
        """Get Pdf page count"""
        try:
            pdf = PdfFileReader(pdf_file)
            return pdf.numPages
        except PdfReadError:
            return 0
