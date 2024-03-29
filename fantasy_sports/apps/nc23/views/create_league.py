from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django import forms
from ..management.commands.roll_transfers import add_transfers

from ..forms import CreateNCLeagueForm
from ..models import League, Manager


class CreateLeague(LoginRequiredMixin, CreateView):
    model = League
    form_class = CreateNCLeagueForm
    http_method_names = [u'get', u'post']
    template_name = 'nc23/create_league.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        form = CreateNCLeagueForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.administrator = request.user
            if not league.is_administrator_valid:
                form.add_error(
                    None,
                    'You may administrate a maximum of {} leagues'.format(
                        League.MAX_LEAGUES_PER_ADMIN
                    )
                )
                return self.form_invalid(form)

            league.save()
            add_transfers(league, [])

            messages.success(
                request,
                "Successfully created league '{}'".format(
                    form.cleaned_data['name']
                )
            )
            return redirect(reverse_lazy('nc23:join_league', args=[str(league.id)]))
        else:
            return self.form_invalid(form)
