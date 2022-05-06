from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django import forms

from ..forms import CreateBoaLeagueForm
from ..models import League, Manager


class CreateLeague(LoginRequiredMixin, CreateView):
    model = League
    form_class = CreateBoaLeagueForm
    http_method_names = [u'get', u'post']
    template_name = 'boa/create_league.html'

    widgets = {
        'password': forms.PasswordInput(),
    }

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        form = CreateBoaLeagueForm(request.POST)

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


            messages.success(
                request,
                "Successfully created league '{}'".format(
                    form.cleaned_data['name']
                )
            )
            return redirect(reverse_lazy('boa:join_league', args=[str(league.id)]))
        else:
            return self.form_invalid(form)
