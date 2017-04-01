from django.shortcuts import render
from django.views.generic import TemplateView


class Hello(TemplateView):
    template_name = 'tennis/hello.html'

    def get_context_data(self, **kwargs):
        context = super(Hello, self).get_context_data(**kwargs)
        context.update({'my_word': "well hello there"})
        return context

    def get(self, request, *args, **kwargs):
        return super(Hello, self).get(request, *args, **kwargs)
