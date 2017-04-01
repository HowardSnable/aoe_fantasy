from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.urlresolvers import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class FantasySportsCreateAccountForm(forms.ModelForm):
    verify_password = forms.CharField(
                          label='Confirm Password',
                          widget=forms.PasswordInput(),
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
        super(FantasySportsCreateAccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('account_management:create')
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'verify_password',
            Submit('submit', 'Creat Account', css_class='col-xs-offset-4'),
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('This field is required.')

        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError('This email is already registered.')

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('This field is required.')

        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise forms.ValidationError('This username is already in use.')

        return username

    def clean_verify_password(self):
        password = self.cleaned_data.get('password')
        verify_password = self.cleaned_data.get('verify_password')
        if password and verify_password and password != verify_password:
            raise forms.ValidationError('Passwords do not match.')

        validate_password(verify_password)

        return verify_password


class FantasySportsAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FantasySportsAuthenticationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('account_management:login')
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login', css_class='col-xs-offset-4'),
        )


class FantasySportsPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(FantasySportsPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = \
            "If found, we'll email instructions to reset your password."

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('account_management:password_reset')
        self.helper.layout = Layout(
            'email',
            Submit('submit', 'Reset Password', css_class='col-xs-offset-4'),
        )


class FantasySportsSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(FantasySportsSetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'new_password1',
            'new_password2',
            Submit('submit', 'Change Password', css_class='col-xs-offset-4'),
        )
