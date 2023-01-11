from django.shortcuts import redirect, reverse


def redirect_view(request):
    return redirect(reverse('nc23:home'))
