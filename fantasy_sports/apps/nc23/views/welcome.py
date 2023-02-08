from django.views.generic import TemplateView

from ..constants import *


class WelcomeView(TemplateView):
    http_method_names = [u'get']
    template_name = 'nc23/welcome.html'

    def get_context_data(self, **kwargs):
        context = {}


        return context
