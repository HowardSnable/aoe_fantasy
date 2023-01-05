from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from datetime import date
from .filters import subtract_date

from ..forms import FindNCLeagueForm
from ..models import League


class FindLeague(LoginRequiredMixin, ListView):
    model = League
    form_class = FindNCLeagueForm
    http_method_names = [u'get', u'post']
    template_name = 'nc23/find_league.html'
    success_url = reverse_lazy('nc23:find_league')
    leagues = []

    def get_context_data(self, **kwargs):
        context = super(FindLeague, self).get_context_data(**kwargs)

        if not self.leagues:
            full_league_ids = [ll.id for ll in League.objects.all() if ll.is_full() == True]
            self.leagues = League.objects.exclude(id__in=full_league_ids)
        context.update({
            'leagues': self.leagues,
            'form': FindNCLeagueForm(),
            'today': date.today()
        })
        return context

    def get(self, request, *args, **kwargs):
        return super(FindLeague, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = FindNCLeagueForm(request.POST or None)
        self.object_list = self.get_queryset()
        if form.is_valid():
            full_league_ids = [ll.id for ll in League.objects.all() if ll.is_full() == True]
            self.leagues = League.objects.\
                filter(name__icontains=form.cleaned_data.get('name')).\
                exclude(id__in=full_league_ids)

            if not self.leagues:
                messages.info(
                    request,
                    'No leagues found.'
                )
        else:
            self.leagues = League.objects.filter(is_full=False)
        return self.render_to_response(self.get_context_data())

