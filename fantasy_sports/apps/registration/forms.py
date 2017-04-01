from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.urlresolvers import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class CreateAccountForm(forms.ModelForm):
    verify_password = forms.CharField(
                          label='Confirm Password',
                          widget=forms.PasswordInput,
                          required=True,
                      )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
        )

        widgets = {
            'password': forms.PasswordInput(),
        }

        help_texts = {
            'username': '',
        }

    def __init__(self, *args, **kwargs):
        super(CreateAccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('registration:create')
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'verify_password',
            Submit('submit', 'Creat Account', css_class='col-xs-offset-4'),
        )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("Please enter your first name")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError('Please enter your last name')

        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Please enter your email')

        email_already_exists = User.objects.filter(email=email).exists()
        if email_already_exists:
            raise forms.ValidationError('This email is already registered')

        return email

    def clean_verify_password(self):
        password = self.cleaned_data.get('password')
        verify_password = self.cleaned_data.get('verify_password')
        if password and verify_password and password != verify_password:
            raise forms.ValidationError('Passwords do not match')

        validate_password(verify_password)

        return verify_password


class RegistrationLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationLoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('registration:login')
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login', css_class='col-xs-offset-4'),
        )


class RegistrationPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = \
            "If found, we'll email instructions on resetting your password."

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('registration:password_reset')
        self.helper.layout = Layout(
            'email',
            Submit('submit', 'Reset Password', css_class='col-xs-offset-4'),
        )
