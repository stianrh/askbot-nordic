"""file utilities for askbot"""
import os
import random
import time
import urlparse
from django.core.files.storage import get_storage_class
from django.core.urlresolvers import reverse
from django.conf import settings as django_settings
from askbot.models.attachment import Attachment

def store_file(file_object, file_name_prefix = ''):
    """Creates an instance of django's file storage
    object based on the file-like object,
    returns the storage object, file name, file url
    """
    attachment = Attachment(filename=file_object.name)
    attachment.save()

    # use default storage to store file
    file_storage = get_storage_class()()
    file_storage.save(attachment.filehash, file_object)

    file_url = reverse('get_attachment', kwargs={'filehash': attachment.filehash})

    return file_storage, attachment.filehash, file_url
