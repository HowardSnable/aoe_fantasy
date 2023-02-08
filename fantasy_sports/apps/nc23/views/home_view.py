from django.shortcuts import redirect, reverse


def home_view(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect(reverse('nc23:my_leagues'))
    return redirect(reverse('nc23:welcome'))
