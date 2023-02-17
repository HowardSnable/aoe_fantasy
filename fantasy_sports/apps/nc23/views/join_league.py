from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView

from ..forms import CreateNCLeagueForm, JoinNCLeagueForm
from ..models import League, Manager
from .team_names import *

import random


def roll_team_name():
    prefix = random.choice(['', 'The', random.choice(PREFIXES)])
    return f'{prefix} {random.choice(MIDFIXES)} {random.choice(SUFFIXES)}'


class JoinLeague(LoginRequiredMixin, CreateView):
    model = Manager
    form_class = JoinNCLeagueForm
    http_method_names = [u'get', u'post']
    template_name = 'nc23/join_league.html'
    object = None

    def get(self, request, *args, **kwargs):
        context = {}
        my_league_id = kwargs['pk']
        league = League.objects.get(id=my_league_id)

        initial_data = {'name': roll_team_name()}

        if league.password:
            form = JoinNCLeagueForm(pw=True, initial=initial_data)
        else:
            form = JoinNCLeagueForm(pw=False, initial=initial_data)

        context.update({
            'league': league,
            'form': form,
        })
        return self.render_to_response(context)

    def get_success_url(self):
        return self.object.league.get_absolute_url()

    def post(self, request, *args, **kwargs):
        
        if not 'submit' in request.POST:
             return self.get(request, *args, **kwargs)

        my_league_id = kwargs['pk']
        league = League.objects.get(id=my_league_id)

        has_password = bool(league.password)
        form = JoinNCLeagueForm(request.POST, pw=has_password)

        if form.is_valid():

            manager = form.save(commit=False)
            manager.league = league
            manager.user = self.request.user

            # check password
            if league.password and not('password' in form.cleaned_data
                                       and form.cleaned_data['password'] == league.password):
                form.add_error(
                    None,
                    f'Invalid password.'
                )
                return self.form_invalid(form)

            #check team count
            if Manager.objects.filter(league=league).count() >= league.max_teams_per_league:
                form.add_error(
                    None,
                    f'This league is full.'
                )
                return self.form_invalid(form)

            #check if already in league and team name
            for other_manager in Manager.objects.filter(league=league):
                if manager.user == other_manager.user:
                    form.add_error(
                        None,
                        f'You already manage a team in this league'
                    )
                    return self.form_invalid(form)

                if manager.name == other_manager.name:
                    form.add_error(
                        None,
                        f'There is already a team named {manager.name} in this league'
                    )
                    return self.form_invalid(form)

            manager.save()

            messages.success(
                request,
                f'Successfully joined league {league}'
                )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
