# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from .models import MembershipRequest, AttachedFile
from utils.render_to_pdf import render_to_pdf


class ViewAttachmentPDF(View):

    def get(self, request, id, *args, **kwargs):
        attachment_id = id
        if attachment_id:
            attachment = AttachedFile.objects.filter(pk=attachment_id).first()
            if attachment:
                if attachment.file.file.name.lower().endswith(('.pdf', )):

                    response = HttpResponse(attachment.file.file, content_type='application/pdf')
                    filename = "formulario_de_registro.pdf"
                    content = "inline; filename='{}'".format(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename='{}'".format(filename)
                    response['Content-Disposition'] = content
                    return response

                else:
                    url = attachment.file.url
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
                                content = "attachment; filename='{}'".format(filename)
                            response['Content-Disposition'] = content
                            return response
        return HttpResponse("Not found")


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        request_id = request.GET.get('id', None)
        if request_id:
            membership_request = MembershipRequest.objects.filter(pk=request_id).first()
            if membership_request:
                context = membership_request.pdf_context
                if context is not None:
                    pdf = render_to_pdf('form2pdf.html', context)
                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        filename = "formulario_de_registro.pdf"
                        content = "inline; filename='{}'" .format(filename)
                        download = request.GET.get("download")
                        if download:
                            content = "attachment; filename='{}'".format(filename)
                        response['Content-Disposition'] = content
                        return response
        return HttpResponse("Not found")
