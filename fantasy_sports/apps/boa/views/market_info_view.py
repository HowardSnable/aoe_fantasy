from django.views.generic import TemplateView
import datetime
from ..models import Team, Player


class MarketInfoView(TemplateView):
    http_method_names = [u'get']
    template_name = 'boa/results.html'

    def get_context_data(self, **kwargs):
        context = {}
        Players = Player.objects.all()
        Teams = Team.objects.all()

        t_start = datetime.datetime.utcnow()
        t_end = datetime.datetime.utcnow() - datetime.timedelta(days=7)

        context.update({
            'teams': zip(Teams, [t.get_top_worth(t_start, t_end) for t in Teams]),
            'payers': zip(Players, [p.get_networth(t_start, t_end) for p in Players]),
        })

        return context
