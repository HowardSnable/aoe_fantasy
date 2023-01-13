from django.views.generic import TemplateView
import datetime
from ..models import Team, Player


class MarketInfoView(TemplateView):
    http_method_names = [u'get']
    template_name = 'nc23/market_info.html'

    def get_context_data(self, **kwargs):
        context = {}
        players = Player.objects.all()
        teams = Team.objects.all()
        team_players = [Player.objects.filter(team=team) for team in teams]

        t_end = datetime.datetime.utcnow()
        t_start = datetime.datetime.utcnow() - datetime.timedelta(days=7)

        player_data = zip(players, [p.networth(t_start, t_end) for p in players])
        player_data = sorted(player_data, key=lambda x: x[1], reverse=True)
        team_data = zip(teams, team_players, [t.get_top_worth(t_start, t_end, 4) for t in teams])
        team_data = sorted(team_data, key=lambda x: x[2], reverse=True)

        context.update({
            'team_data': team_data,
            'player_data': player_data,
        })

        return context
