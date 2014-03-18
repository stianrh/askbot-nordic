from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class AskbotApphook(CMSApp):
    name = _('Askbot apphook')
    urls = ['askbot.urls']

apphook_pool.register(AskbotApphook)
