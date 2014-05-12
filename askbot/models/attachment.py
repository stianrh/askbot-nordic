from django.contrib import admin
from django.db import models, IntegrityError
import os
from binascii import hexlify

def _create_hash():
    return hexlify(os.urandom(16))

class Attachment(models.Model):
    filehash = models.CharField(max_length=200, default=_create_hash, unique=True)
    filename = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        tries = 0
        while tries < 5:
            try:
                super(Attachment, self).save(*args, **kwargs)
                break
            except IntegrityError, e:
                # hash already used
                self.filehash = _create_hash()
        else:
            raise IntegrityError("Could not make a hash for attachment, last tried %s" % (self.filehash, ))

    def __unicode__(self):
        return "<Attachment: %s, hash: %s>" % (self.filename, self.filehash)

    class Meta:
        app_label = 'askbot'

admin.site.register(Attachment)
