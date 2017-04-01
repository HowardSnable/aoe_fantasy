from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView

from ..forms import CreateTennisLeagueForm
from ..models import League


class CreateLeague(LoginRequiredMixin, CreateView):
    model = League
    form_class = CreateTennisLeagueForm
    http_method_names = [u'get', u'post']
    template_name = 'tennis/create_league.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CreateTennisLeagueForm(request.POST)

        if form.is_valid():
            league = form.save(commit=False)
            league.administrator = request.user
            if not league.is_administrator_valid:
                form.add_error(
                    None,
                    'You may administrate a maximum of {} tennis leagues'.format(
                        League.MAX_LEAGUES_PER_ADMIN
                    )
                )
                return self.form_invalid(form)

            league.save()
            messages.success(
                request,
                "Successfully created league '{}'".format(
                    form.cleaned_data['name']
                )
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
