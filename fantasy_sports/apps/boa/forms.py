import datetime

from django import forms
from django.forms import ModelChoiceField
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import League, Manager, TransferMarket, Player


class CreateBoaLeagueForm(forms.ModelForm):

    team_name = forms.CharField(label='Team Name',
                                max_length=20,
                                widget=forms.TextInput(),
                                required=True,) # todo not working

    class Meta:
        model = League
        fields = (
            'name',
            'max_teams_per_league',
            'is_public',
        )

        labels = {
            'name': 'League name',
            'max_teams_per_league': 'Number of teams in league',
            'is_public': 'Publicly visible',
        }

        help_texts = {
            'is_public': 'Will this league be publicly visible?',
        }

        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super(CreateBoaLeagueForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'max_teams_per_league',
            'max_players_per_team',
            'points_per_match_win',
            'is_public',
            Submit('submit', 'Create League', css_class='col-xs-offset-4'),
        )


class UpdateBoaLeagueForm(CreateBoaLeagueForm):

    def __init__(self, *args, **kwargs):
        super(UpdateBoaLeagueForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'max_teams_per_league',
            'is_public',
            Submit('submit', 'Update League', css_class='col-xs-offset-4'),
        )


class FindBoaLeagueForm(forms.ModelForm):

    class Meta:
        model = League
        fields = (
            'name',
        )

        labels = {
            'name': 'Search by league name',
        }

    def __init__(self, *args, **kwargs):
        super(FindBoaLeagueForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('boa:find_league')
        self.helper.layout = Layout(
            'name',
            Submit('submit', 'Find League', css_class='col-xs-offset-4'),
        )


class PlayerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CreateOfferForm(forms.Form):
    player = PlayerChoiceField(widget=forms.Select(),
                               queryset=Player.objects.all(),
                               label="",
                               empty_label=None)
    price = forms.IntegerField(widget=forms.NumberInput)
    end_date = forms.DateTimeField(initial=datetime.datetime.now()+datetime.timedelta(days=1),
                                   widget=forms.DateTimeInput())

    def __init__(self, *args, **kwargs):
        super(CreateOfferForm, self).__init__(*args, **kwargs)

