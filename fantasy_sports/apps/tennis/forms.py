from django import forms
from django.core.urlresolvers import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import League


class CreateTennisLeagueForm(forms.ModelForm):

    class Meta:
        model = League
        fields = (
            'name',
            'max_teams_per_league',
            'max_players_per_team',
            'max_injured_players_per_team',
            'is_public',
            'points_per_match_win',
            'tournament_win_bonus',
            'grand_slam_point_multiplier',
        )

        labels = {
            'name': 'League name',
            'max_teams_per_league': 'Number of teams in league',
            'max_players_per_team': 'Number of players per team',
            'max_injured_players_per_team': 'Number of injury spots per team',
            'is_public': 'Publicly visible',
            'points_per_match_win': 'Points per match win',
            'tournament_win_bonus': 'Tournament win bonus',
            'grand_slam_point_multiplier': 'Grand Slam point multiplier',
        }

        help_texts = {
            'is_public': 'Will this league be publicly visible?',
            'points_per_match_win': 'How many points will a player earn for winning a match?',
            'tournament_win_bonus': 'How many bonus points will a player earn for winning a tournament?',
            'grand_slam_point_multiplier': 'Points earned in Grand Slams will be multipied by this number.',
        }

        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super(CreateTennisLeagueForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'max_teams_per_league',
            'max_players_per_team',
            'max_injured_players_per_team',
            'points_per_match_win',
            'tournament_win_bonus',
            'grand_slam_point_multiplier',
            'is_public',
            Submit('submit', 'Create League', css_class='col-xs-offset-4'),
        )


class UpdateTennisLeagueForm(CreateTennisLeagueForm):

    def __init__(self, *args, **kwargs):
        super(UpdateTennisLeagueForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'max_teams_per_league',
            'max_players_per_team',
            'max_injured_players_per_team',
            'points_per_match_win',
            'tournament_win_bonus',
            'grand_slam_point_multiplier',
            'is_public',
            Submit('submit', 'Update League', css_class='col-xs-offset-4'),
        )


class FindTennisLeagueForm(forms.ModelForm):

    class Meta:
        model = League
        fields = (
            'name',
        )

        labels = {
            'name': 'Search by league name',
        }

    def __init__(self, *args, **kwargs):
        super(FindTennisLeagueForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('tennis:find_league')
        self.helper.layout = Layout(
            'name',
            Submit('submit', 'Find League', css_class='col-xs-offset-4'),
        )
