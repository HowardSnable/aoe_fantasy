import collections

from django import forms
from django.forms import ModelChoiceField
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import League, Manager, LineUp, Player


class CreateBoaLeagueForm(forms.ModelForm):

    class Meta:
        model = League
        fields = (
            'name',
            'max_teams_per_league',
            'is_public',
            'password',
        )

        labels = {
            'name': 'League name',
            'max_teams_per_league': 'Number of teams in league',
            'is_public': 'Publicly visible',
            'password': 'Password',
        }

        help_texts = {
            'is_public': 'Will this league be publicly visible?',
            'password': 'Set a password if you want the league to be private',
        }

        widgets = {
            'password': forms.PasswordInput(),
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
            'password',
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
            'transfers_per_day',
            'is_public',
            Submit('submit', 'Update League', css_class='col-xs-offset-4'),
        )


class FindBoaLeagueForm(forms.Form):

    name = forms.CharField(max_length=20, label="", required=False)

    def __init__(self, *args, **kwargs):
        super(FindBoaLeagueForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'col-xs-6'
        self.helper.field_class = 'col-xs-4'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('boa:find_league')
        self.helper.layout = Layout(
            'name',
            Submit('submit', 'Find League', css_class='col-xs'),
        )


class JoinBoaLeagueForm(forms.ModelForm):

    class Meta:
        model = Manager
        fields = (
            'name',
        )

        labels = {
            'name': 'Team name',
        }

        help_texts = {
        }

        widgets = {
        }

    def __init__(self, *args, **kwargs):
        if "pw" in kwargs:
            pw = kwargs.pop("pw")
        else:
            pw = False
        super(JoinBoaLeagueForm, self).__init__(*args, **kwargs)

        if pw:
            # add password field
            password_field = forms.CharField(widget=forms.PasswordInput, label="Password:")
            fields = list(self.fields.items())
            fields.append(('password', password_field))
            self.fields = collections.OrderedDict(fields)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'

        if pw:
            self.helper.layout = Layout('name',
                                        'password',
                                        Submit('submit', 'Join League', css_class='col-xs-offset-4'), )
        else:
            self.helper.layout = Layout('name',
                                        Submit('submit', 'Join League', css_class='col-xs-offset-4'), )



class PlayerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CreateOfferForm(forms.Form):
    player = PlayerChoiceField(widget=forms.Select(),
                               queryset=Player.objects.all(),
                               label="",
                               empty_label=None)
    price = forms.IntegerField(widget=forms.NumberInput)

    def __init__(self, *args, **kwargs):
        tr_players = kwargs.pop('tr_players')
        super(CreateOfferForm, self).__init__(*args, **kwargs)
        self.fields['player'].choices = tr_players


class CreateTransferForm(forms.Form):
    player = PlayerChoiceField(widget=forms.Select(),
                               queryset=Player.objects.all(),
                               label="Player",
                               empty_label=None)
    price = forms.IntegerField(widget=forms.NumberInput)

    def __init__(self, *args, **kwargs):
        tr_players = kwargs.pop('tr_players')
        super(CreateTransferForm, self).__init__(*args, **kwargs)
        self.fields['player'].choices = tr_players


CAPTAIN_CHOICES = [(LineUp.FLANK1, 'C'),
                   (LineUp.POCKET, 'C'),
                   (LineUp.FLANK2, 'C'),
                   (LineUp.NONE, 'No Captain')]


class RadioTableRenderer(forms.RadioSelect):
    def render(self):
        return (mark_safe(u''.join([u'<td>%s</td>' % force_unicode(w.tag()) for w in self])))

class CreateLineUpForm(forms.Form):
    flank1 = PlayerChoiceField(widget=forms.Select(),
                               queryset=Player.objects.all(),
                               label="Flank",
                               empty_label=None,
                               required=False)
    pocket = PlayerChoiceField(widget=forms.Select(),
                               queryset=Player.objects.all(),
                               label="Pocket",
                               empty_label=None,
                               required=False)
    flank2 = PlayerChoiceField(widget=forms.Select(),
                               queryset=Player.objects.all(),
                               label="Flank",
                               empty_label=None,
                               required=False)
    captain = forms.IntegerField(label='Captain',
                                 widget=RadioTableRenderer(choices=CAPTAIN_CHOICES))

    def __init__(self, *args, **kwargs):
        if 'team_players' in kwargs:
            team_players = kwargs.pop('team_players')
            super(CreateLineUpForm, self).__init__(*args, **kwargs)
            self.fields['flank1'].choices = team_players
            self.fields['pocket'].choices = team_players
            self.fields['flank2'].choices = team_players
        else:
            super(CreateLineUpForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        flank1 = cd.get('flank1')
        pocket = cd.get('pocket')
        flank2 = cd.get('flank2')

        players = [flank1, pocket, flank2]
        players = list(filter(None, players))

        if not any(players):
            raise ValidationError("No player selected")

        if len(players) != len(set(players)):
            raise ValidationError("Cannot filed the same player twice!")

        return cd
