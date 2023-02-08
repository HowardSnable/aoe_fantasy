from django.views.generic import TemplateView

from ..constants import *
from django.shortcuts import render

def welcome_view(request):
    http_method_names = [u'get']
    template_name = 'nc23/welcome.html'
    return render(request, template_name, {})
