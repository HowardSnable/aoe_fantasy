from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib import messages

import datetime

from ..models import Poll, Vote
from ..forms import VoteForm


def get_polls():
    dtime = datetime.datetime.utcnow()
    future_polls = Poll.objects.filter(start__gte=dtime).order_by('start')
    if future_polls:
        next_poll_start = future_polls.first().start
    else:
        next_poll_start = None
    return (Poll.objects.get(start__lte=dtime, end__gte=dtime),
            Poll.objects.filter(end__lte=dtime),
            next_poll_start
            )


def get_vote(user, poll):
    return (Vote.objects
            .filter(poll=poll)
            .get(user=user)
            )


class VoteView(LoginRequiredMixin, View):
    http_method_names = [u'get']
    template_name = 'nc23/vote.html'

    def get_context_data(self):
        context = {}

        user = self.request.user
        poll, old_polls, next_poll_start = get_polls()
        context.update({
            'current_poll': poll,
            'user': user,
            'old_polls': old_polls
        })
        if not poll:
            context.update({'next_poll_date': next_poll_start})
            return context

        #
        form = VoteForm()
        vote = get_vote(user, poll)
        context.update({
            'form': form,
            'vote': vote,
        })

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        context = self.get_context_data()
        if request.GET.get('delete_button'):
            vote = context.get('vote')
            vote.delete()

            messages.success(
                request,
                'Vote deleted.'
            )
            # reload context without vote
            context = self.get_context_data()
            return context

        # add vote
        voted_player = request.POST.get("voted_player")
        vote = Vote(poll=context.get("poll"),
                    player=voted_player,
                    user=request.POST.user)
        vote.save()

        context = self.get_context_data()
        return context
