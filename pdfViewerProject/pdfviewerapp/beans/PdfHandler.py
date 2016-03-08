import base64
import os
from pdfviewerapp.models import FichierPdf


class PdfHandler(object):
    """
    PDF Management class
    """

    def __init__(self, id_pdf):
        self.id_pdf = id_pdf
        self.images = []
        self.error = None
        self.nb_pages = 0


    # Extrait les images du pdf et les cree sous la forme image1.xxx, image2.xxx, ...
    def extract_images(self, start, end, quality=72):
        """
        Extract images from pdf file
        :param start: index of first page
        :param end: index of last page
        :param quality: density
        :return:
        """
        try:
            pdf_file = FichierPdf.objects.get(pk=self.id_pdf)
        except FichierPdf.DoesNotExist:
            self.error = 'Invalid pdf file id'
            return

        nb_pages = pdf_file.nb_pages
        pdf_path = pdf_file.pdf_file.path

        if end > nb_pages:
            end = nb_pages
        if end < start:
            end = start

        if not self.valid_pages(start, end, nb_pages):
            self.error = 'Invalid page index range'
            return
        self.nb_pages = nb_pages

        for index in xrange(start, end + 1):
            img_file_name = "media/pdf_imgs/pdf_{}_{}_{}.png".format(self.id_pdf, quality, index)

            try:
                b64_img = self.image_to_base64(img_file_name)
                self.images.append(b64_img)
            except IOError:
                args = [
                    'ghostscript'
                    ' -dNumRenderingThreads=4'
                    ' -q',
                    ' -dNOGC',
                    ' -dNOPAUSE',
                    ' -dBATCH',
                    ' -dSAFER',
                    ' -dNOTRANSPARENCY',
                    ' -sDEVICE=pngalpha',
                    ' -r{}'.format(quality),
                    ' -dFirstPage={}'.format(index),
                    ' -dLastPage={}'.format(index),
                    ' -dGraphicsAlphaBits=4',
                    ' -dTextAlphaBits=4',
                    ' -sOutputFile={}'.format(img_file_name),
                    ' %s' % pdf_path,  # Source
                ]
                cmd = ' '.join(args)
                os.system(cmd)
                self.images.append(self.image_to_base64(img_file_name))

    @staticmethod
    def valid_pages(start, end, nbpages):
        """Check pages range"""
        return 0 < start <= nbpages and 0 < end <= nbpages

    @staticmethod
    def image_to_base64(path):
        """Convert image to base64"""
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read())
