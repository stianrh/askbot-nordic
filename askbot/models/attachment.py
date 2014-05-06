from django.db import models

class Attachment(models.Model):
    filehash = models.CharField(max_length=200, unique=True)
    filename = models.CharField(max_length=200)

    class Meta:
        app_label = 'askbot'


