from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from utils.logs import build_log
from PIL import Image
import pytesseract
import argparse
import numpy as np
import urllib
import cv2
import os
from datetime import datetime

from crum import get_current_user


class OCRRequest(models.Model):
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.ForeignKey(User, null=False, related_name="ocr_request_created")
    updated_by = models.ForeignKey(User, null=True, related_name="ocr_request_updated")
    image = models.ImageField(upload_to='OCR/images/')
    result = models.TextField()
    working_path = models.TextField()
    log = JSONField(default=list([]), null=False)

    def save(self, owner=False, *args, **kwargs):
        if owner:
            user = self.created_by
        else:
            user = get_current_user()

        if user is None or not user.is_authenticated and not owner:
            raise ValidationError(_('Need to be log into the system to create a OCR Request'))

        if self.pk is None:
            self.created_by = user
            self.log = [build_log(user, _('Created the OCR Request'))]
        else:
            self.updated_by = user
            log = self.log + [build_log(user, _('Updated the OCR Request'))]
            self.log = log
        super(OCRRequest, self).save(*args, **kwargs)

    @property
    def process(self):
        self.generate_working_path
        if self.working_path is not None or os.path.exists("{}/{}".format(os.getcwd(), self.working_path)) and \
                        self.image is not None:
            url = self.image.url
            resp = urllib.request.urlopen(url)

            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            filename = "{}/{}.png".format(self.working_path , datetime.now().strftime('%Y%m%d%H%M%s'))
            cv2.imwrite(filename, gray)
            user = get_current_user()
            try:
                text = pytesseract.image_to_string(Image.open(filename))
                self.result = text
                log = self.log + [build_log(self.created_by, _('Image has been processed for OCR'))]
                self.log = log
                self.save(owner=True)
            except Exception as e:
                print("{}".format(e))

    @property
    def generate_working_path(self):
        if self.working_path is None or not os.path.exists("{}/{}".format(os.getcwd(), self.working_path)):
            path = "{}/{}-{}".format(os.getcwd(), self.pk, datetime.now().strftime('%Y%m%d%H%M%s'))
            if not os.path.exists(path):
                os.makedirs(path)
            self.working_path = path
            self.save(owner=True)
