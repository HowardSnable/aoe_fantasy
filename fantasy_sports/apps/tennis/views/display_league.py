from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from ..models import League


class DisplayLeague(LoginRequiredMixin, DetailView):
    http_method_names = [u'get']
    template_name = 'tennis/display_league.html'
    model = League

    def get_context_data(self, **kwargs):
        return super(DisplayLeague, self).get_context_data(**kwargs)
