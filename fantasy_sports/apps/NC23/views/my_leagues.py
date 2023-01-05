from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..models import League


class MyLeagues(LoginRequiredMixin, TemplateView):
    http_method_names = [u'get']
    template_name = 'nc23/my_leagues.html'

    def get_context_data(self, **kwargs):
        context = {}

        admin_leagues = League.objects.filter(
            administrator=self.request.user,
        )
        non_admin_leagues = League.objects.filter(
            manager__user=self.request.user,
        )

        in_a_league = admin_leagues.exists() or non_admin_leagues.exists()

        context.update({
            'admin_leagues': admin_leagues,
            'non_admin_leagues': non_admin_leagues,
            'in_a_league': in_a_league,
        })

        return context
