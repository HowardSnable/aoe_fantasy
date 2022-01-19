from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from ..forms import FindBoaLeagueForm
from ..models import League


class FindLeague(LoginRequiredMixin, FormView):
    form_class = FindBoaLeagueForm
    http_method_names = [u'get', u'post']
    template_name = 'boa/find_league.html'
    success_url = reverse_lazy('boa:find_league')

    def get_context_data(self, **kwargs):
        context = super(FindLeague, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return super(FindLeague, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = FindBoaLeagueForm(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
