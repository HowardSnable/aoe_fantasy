from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..models import Result, MatchDay


class ResultView(TemplateView):
    http_method_names = [u'get']
    template_name = 'nc23/results.html'

    def get_context_data(self, **kwargs):
        context = {}

        results = {}
        matchdays = MatchDay.objects.filter(is_booked=True)
        results[0] = Result.objects.all().order_by('player__team')
        for mday in matchdays:
            results[mday.id] = Result.objects.filter(matchday=mday).order_by('player__team')

        context.update({
            'matchdays': matchdays,
            'results': results,
        })

        return context
