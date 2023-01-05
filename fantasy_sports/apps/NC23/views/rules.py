from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..constants import *


class RulesView(TemplateView):
    http_method_names = [u'get']
    template_name = 'nc23/rules.html'

    def get_context_data(self, **kwargs):
        context = {}

        context.update({
            'POINTS_PER_MATCH_WIN': POINTS_PER_MATCH_WIN,
            'POINTS_PER_MATCH_LOSS': POINTS_PER_MATCH_LOSS,
            'POINT_FOR_MVP': POINT_FOR_MVP,
            'CAPTAIN_FACTOR': CAPTAIN_FACTOR,
            'POINTS_FOR_POSITION': POINTS_FOR_POSITION,
            'POINT_FOR_MVP': POINT_FOR_MVP,
            'POINTS_FOR_EMPTY': POINTS_FOR_EMPTY,
        })

        return context
