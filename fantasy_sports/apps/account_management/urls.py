from django.urls import re_path
from django.contrib.auth import views as auth_views

from . import views as account_management_views
from .forms import (
    FantasySportsAuthenticationForm,
    FantasySportsChangePasswordForm,
    FantasySportsPasswordResetForm,
    FantasySportsSetPasswordForm,
)

app_name = 'account_management'

urlpatterns = [
    re_path(
        '^create/$',
        account_management_views.CreateAccount.as_view(),
        name='create',
    ),
    re_path(
        '^login/$',
        auth_views.LoginView.as_view(template_name='account_management/login.html',
                                     authentication_form=FantasySportsAuthenticationForm,
                                     redirect_authenticated_user=True),
        name='login',
    ),
    re_path(
        '^logout/$',
        auth_views.LogoutView.as_view(template_name='account_management/logout.html'),
        name='logout',
    ),
    re_path(
        '^change_password/$',
        auth_views.PasswordChangeView.as_view(template_name='account_management/change_password.html',
                                              success_url='account_management:change_password_complete',
                                              form_class=FantasySportsChangePasswordForm),
        name='change_password',
    ),
    re_path(
        '^change_password/complete/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='account_management/change_password_complete.html'),
        name='change_password_complete',
    ),
    re_path(
        '^password_reset/$',
        auth_views.PasswordResetView.as_view(template_name='account_management/password_reset.html',
                                             email_template_name='account_management/password_reset.email',
                                             success_url='account_management:password_reset_sent',
                                             form_class=FantasySportsPasswordResetForm),
        name='password_reset',
    ),
    re_path(
        '^password_reset/sent/$',
        auth_views.PasswordResetDoneView.as_view(template_name='account_management/password_reset_sent.html'),
        name='password_reset_sent',
    ),
    re_path(
        '^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
                                    template_name='account_management/password_reset_change_password.html',
                                    form_class=FantasySportsSetPasswordForm,
                                    success_url='account_management:password_reset_complete'
        ),
        name='password_reset_confirm',
    ),
    re_path(
        '^password_reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='account_management/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]
