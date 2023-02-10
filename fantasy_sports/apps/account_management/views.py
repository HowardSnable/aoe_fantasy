from django.contrib import messages
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import FantasySportsCreateAccountForm


class CreateAccount(FormView):
    form_class = FantasySportsCreateAccountForm
    http_method_names = [u'get', u'post']
    template_name = 'account_management/create_account.html'
    success_url = reverse_lazy('account_management:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # create user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
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
