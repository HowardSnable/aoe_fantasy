from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from ..forms import FindBoaLeagueForm
from ..models import League


class FindLeague(LoginRequiredMixin, ListView):
    model = League
    form_class = FindBoaLeagueForm
    http_method_names = [u'get', u'post']
    template_name = 'boa/find_league.html'
    success_url = reverse_lazy('boa:find_league')
    leagues = []

    def get_context_data(self, **kwargs):
        context = super(FindLeague, self).get_context_data(**kwargs)

        if not self.leagues:
            self.leagues = League.objects.filter(is_public=True)
        context.update({
            'leagues': self.leagues,
            'form': FindBoaLeagueForm()})
        return context

    def get(self, request, *args, **kwargs):
        return super(FindLeague, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = FindBoaLeagueForm(request.POST or None)
        self.object_list = self.get_queryset()
        if form.is_valid():
            self.leagues = League.objects.filter(name__icontains=form.cleaned_data.get('name'))
            if not self.leagues:
                messages.info(
                    request,
                    'League not found.'
                )
        else:
            self.leagues = League.objects.filter(is_public=True)
        return self.render_to_response(self.get_context_data())

