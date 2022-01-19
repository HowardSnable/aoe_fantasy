from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'boa/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context.update({'my_word': "well hello there"})
        return context

    def get(self, request, *args, **kwargs):
        return super(Home, self).get(request, *args, **kwargs)
