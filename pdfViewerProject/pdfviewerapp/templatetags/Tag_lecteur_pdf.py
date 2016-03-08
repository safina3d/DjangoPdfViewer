from django import template

register = template.Library()


@register.inclusion_tag("templ_tag_lecteur.html")
def lecteur_pdf(*args, **kwargs):
    return {
        'pdfid': kwargs.get('pdfid') or '',
        'res': kwargs.get('res') or '',
        'width': kwargs.get('w') or '',
        'height': kwargs.get('h') or ''
    }
