from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views as registration_views
from .forms import (
    RegistrationLoginForm,
    RegistrationPasswordResetForm,
)


urlpatterns = [
    url(
        '^create/$',
        registration_views.CreateAccount.as_view(),
        name='create'
    ),
    url(
        '^login/$',
        auth_views.login,
        {'authentication_form': RegistrationLoginForm,
         'redirect_authenticated_user': True, },
        name='login',
    ),
    url(
        '^logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.html', },
        name='logout',
    ),
    url(
        '^password_reset/$',
        auth_views.password_reset,
        {'template_name': 'registration/password_reset.html',
         'email_template_name': 'registration/password_reset.email',
         'post_reset_redirect': 'registration:password_reset_done',
         'password_reset_form': RegistrationPasswordResetForm, },
        name='password_reset',
    ),
    url(
        '^password_reset/done/$',
        auth_views.password_reset_done,
        #  {'template_name': 'tennis/hello.html', },
        {'template_name': 'registration/password_reset_done.html', },
        name='password_reset_done',
    ),
    url(
        '^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm.html', },
        name='password_reset_confirm',
    ),
    url(
        '^reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete',
    ),
]
