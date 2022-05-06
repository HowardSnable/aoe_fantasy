from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView

from ..forms import CreateBoaLeagueForm, JoinBoaLeagueForm
from ..models import League, Manager


class JoinLeague(LoginRequiredMixin, CreateView):
    model = Manager
    form_class = JoinBoaLeagueForm
    http_method_names = [u'get', u'post']
    template_name = 'boa/join_league.html'
    object = None

    def get(self, request, *args, **kwargs):
        context = {}
        my_league_id = kwargs['pk']
        league = League.objects.get(id=my_league_id)

        form = JoinBoaLeagueForm()

        context.update({
            'league': league,
            'form': form,
        })
        return self.render_to_response(context)

    def get_success_url(self):
        return self.object.league.get_absolute_url()

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = JoinBoaLeagueForm(request.POST)

        my_league_id = kwargs['pk']
        league = League.objects.get(id=my_league_id)

        if form.is_valid():
            manager = form.save(commit=False)
            manager.league = league
            manager.user = self.request.user

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
