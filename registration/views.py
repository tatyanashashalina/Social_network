from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from config.settings import LOGIN_REDIRECT_URL, LOGIN_URL

from .forms import UserRegistrationForm


def register(request: HttpRequest) -> HttpResponse:
    """
    Registration of user view.

    :param request: client request
    :type request: HttpRequest
    :return: rendered page
    """

    if request.user.is_authenticated:
        return redirect(LOGIN_REDIRECT_URL)

    context: dict = {}

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect(LOGIN_URL)

    else:
        user_form = UserRegistrationForm()

    context['user_form'] = user_form

    return render(request, 'registration/register.html', context)
