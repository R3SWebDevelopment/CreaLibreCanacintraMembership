from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from crum import get_current_user
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from datetime import datetime
from celery import uuid
from utils.zip import unzip
import os
import random
import shutil

PROCESS_STATUS_NULL = 0
PROCESS_STATUS_QUEUED = 1
PROCESS_STATUS_CANCELED = 2
PROCESS_STATUS_PROGRESS = 3
PROCESS_STATUS_COMPLETED = 4
PROCESS_STATUS_ERROR = 5

#
#                         |---------------------------|
#                         |  |-----------|            ^
#                         |  |           ^            |
#                         |  |           |            |
#                         |  |         ERROR          |
#                         |  |           ^            |
#                         V  V           |            |
# PROCESS FLOW  NULL --> QUEUED --> PROGRESS --> COMPLETED
#                         ^  V            |
#                         |  |            V
#                         |  |-------->CANCELED
#                         |                 v
#                         |-----------------|

PROCESS_STATUS = (
    (PROCESS_STATUS_NULL, _('NULL')),
    (PROCESS_STATUS_QUEUED, _('QUEUED')),
    (PROCESS_STATUS_CANCELED, _('CANCELED')),
    (PROCESS_STATUS_PROGRESS, _('PROGRESS')),
    (PROCESS_STATUS_COMPLETED, _('COMPLETED')),
    (PROCESS_STATUS_ERROR, _('ERROR')),
)


def get_current_user_or_none():
    current_user = get_current_user()
    return None if current_user is None else current_user


class HiddenModelQuerySet(models.QuerySet):

    def all(self):
        qs = super(HiddenModelQuerySet, self).all()
        return qs.exclude(hidden=True)


class HiddenModelManager(models.Manager):
    def get_queryset(self):
        return HiddenModelQuerySet(self.model, using=self._db).exclude(hidden=True)


class OwnerModelQuerySet(models.QuerySet):

    def all(self):
        qs = super(OwnerModelQuerySet, self).all()
        current_user = get_current_user()
        if current_user is not None and current_user.is_authenticated:
            if not current_user.is_staff:
                qs = qs.filter(owner=current_user)
            return qs
        return qs.none()


class OwnerModelManager(models.Manager):
    def get_queryset(self):
        return OwnerModelQuerySet(self.model, using=self._db)


class OwnerModel(models.Model):
    owner = models.ForeignKey(User, null=True, default=get_current_user_or_none)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = OwnerModelManager()

    class Meta:
        abstract = True


class CeleryProcessable(models.Model):
    process_id = models.UUIDField(null=True)
    process_status = models.IntegerField(null=False, choices=PROCESS_STATUS, default=PROCESS_STATUS_NULL)
    process_started_at = models.DateTimeField(null=True)
    process_updated_at = models.DateTimeField(null=True)
    process_has_error = models.NullBooleanField(default=None)
    process_error_msg = models.TextField(null=True)
    process_log = ArrayField(JSONField(), default=[])

    class Meta:
        abstract = True

    @classmethod
    def get_process_method(cls):
        raise Exception(_('Need to define process script'))

    def process_start(self):
        if self.process_status in [PROCESS_STATUS_NULL, PROCESS_STATUS_COMPLETED, PROCESS_STATUS_ERROR,
                                   PROCESS_STATUS_CANCELED]:
            process_method = CeleryProcessable.get_process_method()
            task_id = uuid()
            self.process_status = PROCESS_STATUS_QUEUED
            self.process_started_at = datetime.now()
            self.process_updated_at = None
            self.process_id = task_id
            self.set_process_error_msg()
            self.add_process_log(msg="The process its been set on queue to be processed", start=True)
            self.save()
            process_method.apply_async(id=self.id, task_id=task_id)
        else:
            raise Exception(_("This action is not allowed"))

    def add_process_log(self, msg=None, start=False):
        if msg and msg.strip():
            log = [] if start else self.process_log or []
            log.append({
                "timestamp": datetime.now(),
                "msg": msg
            })

    def set_process_error_msg(self, msg=None):
        self.process_error_msg = msg
        self.process_has_error = None if msg is None else True
        if self.process_has_error:
            self.set_process_status(status=PROCESS_STATUS_ERROR)

    def set_process_status(self, status=None):
        if status is not None:
            if status == PROCESS_STATUS_NULL:
                raise Exception(_('This status is not allowed'))
            if status == PROCESS_STATUS_QUEUED:
                self.process_start()
                return
            if status == PROCESS_STATUS_PROGRESS:
                if self.process_status not in [PROCESS_STATUS_QUEUED]:
                    raise Exception(_('This status is not allowed'))
                self.add_process_log(msg="The process has been started")
            if status == PROCESS_STATUS_CANCELED:
                if self.process_status not in [PROCESS_STATUS_QUEUED, PROCESS_STATUS_PROGRESS]:
                    raise Exception(_('This status is not allowed'))
                self.add_process_log(msg="The process has been canceled")
            if status == PROCESS_STATUS_ERROR:
                if self.process_status not in [PROCESS_STATUS_PROGRESS]:
                    raise Exception(_('This status is not allowed'))
                self.add_process_log(msg="The process has been stopped cause an error")
            if status == PROCESS_STATUS_COMPLETED:
                if self.process_status not in [PROCESS_STATUS_PROGRESS]:
                    raise Exception(_('This status is not allowed'))
                self.add_process_log(msg="The process has been completed")
            self.process_status = status
            self.process_updated_at = datetime.now()
            self.save()
        else:
            raise ValueError(_('No Status parameter provided'))


def generate_upload_folder_path(instance, filename):
    app = "{}".format(instance.__class__._meta.app_label)
    model = "{}".format(instance.__class__.__name__)
    prefix = instance.upload_folder_prefix or "compress_file"
    return "{app}/{model}/{prefix}/{filename}".format(**{
        "app": app,
        "model": model,
        "prefix": prefix,
        "filename": filename,
    }).lower()


def generate_decompress_path(instance):
    app = "{}".format(instance.__class__._meta.app_label)
    model = "{}".format(instance.__class__.__name__)
    prefix = instance.upload_folder_prefix or "compress_file"
    id = "{}".format(random.randint(1,100))
    postfix = "{}{}".format("0"*(3-len(id)), id)
    dir_name = "{}_{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), postfix)
    return "{app}/{model}/{prefix}/{dir}/".format(**{
        "app": app,
        "model": model,
        "prefix": prefix,
        "dir": dir_name,
    }).lower()


def build_decompress_path(path):
    base_path = os.getcwd()
    folder_path = "{}/{}".format(base_path, path)
    if not os.path.exists(folder_path):
        try:
            os.mkdir(folder_path)
            return True
        except:
            pass
    return False


class CompressFileUpload(models.Model):
    upload = models.FileField(upload_to=generate_upload_folder_path)
    uncompress_path = models.CharField(max_length=250, null=True)
    listed_files = ArrayField(
        models.CharField(max_length=250, blank=False),
        null=True
    )

    upload_folder_prefix = None  # Set this attr on the child model class to define a prefix fot the upload folder path
    exclude_extensions = []  # Set this attr to exclude certain file extension when decompressing the files
    filter_extensions = []  # Set this attr to filter certain file extension when decompressing the files

    def set_environment(self):
        if not self.uncompress_path_exists():
            self.set_uncompress_path()

    def get_uncompress_path(self):
        base_path = os.getcwd()
        working_path = "{}/{}".format(base_path, self.uncompress_path)
        return working_path

    def clear_environment(self):
        path = self.get_uncompress_path()
        if os.path.exists(path):
            shutil.rmtree(path)

    def extract_files(self):
        unzip(self.upload.file, self.get_uncompress_path())

    def list_uncompressed_files(self):
        base_path = self.get_uncompress_path()
        listed_files = []
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                for f in files:
                    file_path = "{}/{}".format(root, f)
                    filename, file_extension = os.path.splitext(file_path)
                    if self.exclude_extensions and len(self.exclude_extensions) > 0:
                        if file_extension in self.exclude_extensions:
                            continue  # jump to the next item on the loop cause the extension on the exclude list

                    if self.filter_extensions and len(self.filter_extensions) > 0:
                        if file_extension not in self.filter_extensions:
                            continue  # jump to the next item on the loop cause the extension is not on the filter list
                    relative_path = file_path.replace(base_path, '')
                    listed_files.append(relative_path)
        self.listed_files = listed_files
        self.save()

    def get_listed_files(self):
        return self.listed_files or []

    def set_uncompress_path(self):
        break_counter = 100
        while True:
            uncompress_path = generate_decompress_path(self)
            if build_decompress_path(uncompress_path):
                self.uncompress_path = uncompress_path
                self.save()
                return
            if break_counter == 0:
                raise Exception(_("Couldn't create uncompress path"))
            break_counter -= 1

    def uncompress_path_exists(self):
        if self.uncompress_path and self.uncompress_path.strip():
            if os.path.exists(self.uncompress_path) and os.path.isdir(self.uncompress_path):
                return True
        return False

    class Meta:
        abstract = True


class Comment(models.Model):
    source = models.ForeignKey(User, null=True, related_name="comments_sent")
    destination = models.ForeignKey(User, null=True, related_name="comments_received")
    msg = models.TextField(null=True, blank=False)
    timestamp = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        ordering = ('timestamp', )

    def __str__(self):
        return "From: {} - To: {} - When: {}".format(self.source, self.destination, self.timestamp)
