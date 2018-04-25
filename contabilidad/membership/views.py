# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from .models import MembershipRequest
from ..utils import render_to_pdf


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        request_id = self.GET.get('id', None)
        if request_id:
            membership_request = MembershipRequest.objects.filter(pk=request_id).first()
            if membership_request:
                context = membership_request.pdf_context
                if context is not None:
                    pdf = render_to_pdf('form.html', context)
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
