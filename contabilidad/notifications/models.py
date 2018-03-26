from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
import boto3
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime

SNS_ENABLED = settings.SNS_ENABLED or False
SNS_ACCESS_KEY = settings.SNS_ACCESS_KEY or None
SNS_SECRET_ACCESS_KEY = settings.SNS_SECRET_ACCESS_KEY or None
SNS_REGION_NAME = settings.SNS_REGION_NAME or None

FROM_EMAIL_ADDRESS = settings.EMAIL_HOST_USER


def is_sms_enable():
    if SNS_ENABLED and SNS_ACCESS_KEY is not None and SNS_SECRET_ACCESS_KEY is not None and SNS_REGION_NAME is not None:
        return True
    return False


class Notification(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    email = models.BooleanField(default=False)

    email_address = ArrayField(
        models.CharField(max_length=250, null=True)
    )

    email_subject = models.CharField(max_length=250, null=True)
    email_message = models.TextField()
    email_send = JSONField()
    email_has_error = JSONField()
    email_response = JSONField()
    email_error = JSONField()

    sms = models.BooleanField(default=False)

    mobile_number = ArrayField(
        models.CharField(max_length=20, null=True)
    )

    sms_subject = models.CharField(max_length=250, null=True)
    sms_message = models.TextField()
    sms_send = JSONField()
    sms_has_error = JSONField()
    sms_response = JSONField()
    sms_error = models.TextField()

    process_begins = models.DateTimeField(null=True)
    process_began = models.BooleanField(default=False)

    process_ends = models.DateTimeField(null=True)
    process_end = models.BooleanField(default=False)

    @classmethod
    def notify(cls, users, email_subject, email_message, sms_subject, sms_message, sms_override=False,
               email_override=False):
        numbers = []
        mails = []

        if not sms_override:

            if is_sms_enable() and users is not None:
                numbers_list = list(users.objects.filter(profile__notify_by_email=True).
                                    values_list('profile__mobile_number', flat=True))

                for num in numbers_list:
                    number = "{}{}".format(num.get('country_code', ''), num.get('number', ''))
                    if number.strip():
                        numbers.append(number)

        if not email_override:
            mails = list(users.objects.filter(profile__notify_by_sms=True).values_list('email', flat=True))

        if len(numbers) > 0 or len(mails) > 0:
            send_mail = len(mails) > 0
            send_sms = len(numbers) > 0
            notification = cls.objects.create(email=send_mail, sms=send_sms, email_subject=email_subject,
                                              email_message=email_message, sms_subject=sms_subject,
                                              sms_message=sms_message)
            notification.email_address = mails
            notification.mobile_number = numbers
            notification.save()

    def send(self):
        self.process_begins = True
        self.process_began = datetime.now()
        self.save()

        self._send_email()
        self._send_sms()

        self.process_ends = True
        self.process_end = datetime.now()
        self.save()

    def _send_email(self):
        if self.email:
            emails = self.email_address
            if len(emails) > 0:
                email_send = self.email_send or {}
                email_has_error = self.email_has_error or {}
                email_error = self.email_error or {}
                email_response = self.email_response or {}

                message = self.email_message
                subject = self.email_subject

                from_email = FROM_EMAIL_ADDRESS
                text_content = ''
                html_content = message
                msg = EmailMultiAlternatives(subject, text_content, from_email, emails)
                msg.attach_alternative(html_content, "text/html")
                error = False
                error_msg = ""
                response = ""
                try:
                    msg.send()
                    email_send = {email: True for email in emails}
                    email_response = {email: "" for email in emails}
                except Exception as e:
                    error = True
                    error_msg = "{}".format(e)
                    email_send = {email: False for email in emails}
                    email_has_error = {email: True for email in emails}
                    email_error = {email: error_msg for email in emails}

                self.email_send = email_send
                self.email_has_error = email_has_error
                self.email_error = email_error
                self.email_response = email_response
                self.save()

    def _send_sms(self):
        if self.sms:
            numbers = self.mobile_number
            if len(numbers) > 0:
                sms_send = self.sms_send or {}
                sms_has_error = self.sms_has_error or {}
                sms_error = self.sms_error or {}
                sms_response = self.sms_response or {}

                aws_access_key_id = SNS_ACCESS_KEY
                aws_secret_access_key = SNS_SECRET_ACCESS_KEY
                region_name = SNS_ACCESS_KEY
                client = boto3.client('sns', aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key, region_name=region_name)
                message = self.sms_message
                subject = self.sms_subject
                for number in numbers:
                    error = False
                    error_msg = ""
                    try:
                        response = client.publish(PhoneNumber=number, Message=message, Subject=subject)
                    except Exception as e:
                        error = True
                        error_msg = "{}".format(e)
                        response = ""

                    sms_send.update({
                        number: not error
                    })
                    if error:
                        sms_has_error.update({
                            number: True
                        })
                        sms_error.update({
                            number: error_msg
                        })
                    else:
                        sms_response.update({
                            number: response
                        })

                self.sms_send = sms_send
                self.sms_has_error = sms_has_error
                self.sms_error = sms_error
                self.sms_response = sms_response
                self.save()

