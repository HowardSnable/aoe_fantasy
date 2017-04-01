from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views as account_management_views
from .forms import (
    FantasySportsAuthenticationForm,
    FantasySportsChangePasswordForm,
    FantasySportsPasswordResetForm,
    FantasySportsSetPasswordForm,
)


urlpatterns = [
    url(
        '^create/$',
        account_management_views.CreateAccount.as_view(),
        name='create',
    ),
    url(
        '^login/$',
        auth_views.login,
        {'template_name': 'account_management/login.html',
         'authentication_form': FantasySportsAuthenticationForm,
         'redirect_authenticated_user': True, },
        name='login',
    ),
    url(
        '^logout/$',
        auth_views.logout,
        {'template_name': 'account_management/logout.html', },
        name='logout',
    ),
    url(
        '^change_password/$',
        auth_views.password_change,
        {'template_name': 'account_management/change_password.html',
         'post_change_redirect': 'account_management:change_password_complete',
         'password_change_form': FantasySportsChangePasswordForm, },
        name='change_password',
    ),
    url(
        '^change_password/complete/$',
        auth_views.password_change_done,
        {'template_name': 'account_management/change_password_complete.html', },
        name='change_password_complete',
    ),
    url(
        '^password_reset/$',
        auth_views.password_reset,
        {'template_name': 'account_management/password_reset.html',
         'email_template_name': 'account_management/password_reset.email',
         'post_reset_redirect': 'account_management:password_reset_sent',
         'password_reset_form': FantasySportsPasswordResetForm, },
        name='password_reset',
    ),
    url(
        '^password_reset/sent/$',
        auth_views.password_reset_done,
        {'template_name': 'account_management/password_reset_sent.html', },
        name='password_reset_sent',
    ),
    url(
        '^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'account_management/password_reset_change_password.html',
         'set_password_form': FantasySportsSetPasswordForm,
         'post_reset_redirect': 'account_management:password_reset_complete', },
        name='password_reset_confirm',
    ),
    url(
        '^password_reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'account_management/password_reset_complete.html', },
        name='password_reset_complete',
    ),
]
