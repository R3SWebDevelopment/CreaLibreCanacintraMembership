# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from .models import Certification
from utils.render_to_pdf import render_to_pdf


class ViewAttachmentPDF(View):

    def get(self, request, id, *args, **kwargs):
        certification_id = id
        if certification_id:
            certification = Certification.objects.filter(pk=certification_id).first()
            if certification:
                if certification.file.file.name.lower().endswith(('.pdf', )):

                    response = HttpResponse(certification.file.file, content_type='application/pdf')
                    filename = "formulario_de_registro.pdf"
                    content = "inline; filename='{}'".format(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "certification; filename='{}'".format(filename)
                    response['Content-Disposition'] = content
                    return response

                else:
                    url = certification.file.url
                    if url is not None:
                        pdf = render_to_pdf('view_attachment.html', {
                            'image': url,
                        })
                        if pdf:
                            response = HttpResponse(pdf, content_type='application/pdf')
                            filename = "formulario_de_registro.pdf"
                            content = "inline; filename='{}'" .format(filename)
                            download = request.GET.get("download")
                            if download:
                                content = "certification; filename='{}'".format(filename)
                            response['Content-Disposition'] = content
                            return response
        return HttpResponse("Not found")
