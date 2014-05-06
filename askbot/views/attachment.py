import os
from django.http import HttpResponse
from askbot.models.attachment import Attachment
from django.conf import settings
from django.shortcuts import get_object_or_404

def get_attachment(request, filehash):
    a = get_object_or_404(Attachment, filehash=filehash)

    abs_path = "%s/%s" % (settings.PROJECT_ROOT, a.filename)
    
    response = HttpResponse() # 200 OK
    del response['content-type'] # We'll let the web server guess this.
    response['X-Sendfile'] = abs_path
    return response
