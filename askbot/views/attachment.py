import os
import os.path
from django.http import HttpResponse
from askbot.models.attachment import Attachment
from django.conf import settings
from django.shortcuts import get_object_or_404

def get_attachment(request, filehash):
    a = get_object_or_404(Attachment, filehash=filehash)

    abs_path = os.path.join(settings.MEDIA_ROOT, a.filehash)
    
    response = HttpResponse() # 200 OK
    del response['content-type'] # We'll let the web server guess this.
    response['Content-Disposition'] = 'attachment; filename=%s' % a.filename
    response['X-Sendfile'] = abs_path
    return response
