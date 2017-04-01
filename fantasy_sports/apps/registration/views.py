from django.contrib import messages
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from .forms import CreateAccountForm


class CreateAccount(FormView):
    form_class = CreateAccountForm
    http_method_names = [u'get', u'post']
    template_name = 'registration/create_account.html'
    success_url = reverse_lazy('registration:login')

    def get(self, request, *args, **kwargs):
        return super(CreateAccount, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            # create user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            messages.success(
                request,
                "Welcome, {}. You've successfully created an account.".format(
                    user.username
                )
            )
            return self.form_valid(form)

        else:
            return self.form_invalid(form)
