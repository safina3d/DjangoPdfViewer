import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pdfviewerapp.beans import PdfHandler
from models import FichierPdf

def get_pdf_images_service(request):
    """Post Request Processing"""
    if request.method == 'POST':
        data = request.POST.dict()

        pdf_id = data.get('pdf_id')
        from_page = data.get('from_page')
        to_page = data.get('to_page') or from_page
        quality = data.get('quality')
        try:
            pdf_id = int(pdf_id)
            debut = int(from_page)
            fin = int(to_page)
            quality = int(quality)
        except ValueError:
            return JsonResponse({'error':'Invalid POST data'})

        obj = PdfHandler.PdfHandler(pdf_id)
        obj.extract_images(debut, fin, quality=quality)
        return HttpResponse(json.dumps(obj.__dict__))
    else:
        return JsonResponse({'error':'Only POST method supported'})


def index(request):
    """Home page"""
    return render(request, "index.html", {'books': FichierPdf.objects.all()})
