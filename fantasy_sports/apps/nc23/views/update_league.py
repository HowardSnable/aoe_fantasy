from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from ..forms import UpdateNCLeagueForm
from ..models import League


class UpdateLeague(LoginRequiredMixin, UpdateView):
    http_method_names = [u'get', u'post']
    template_name = 'nc23/update_league.html'
    form_class = UpdateNCLeagueForm
    model = League

    def get_context_data(self, **kwargs):
        return super(UpdateLeague, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('nc23:display_league', kwargs=self.kwargs)
