from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from config.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL


def login_page(request: HttpRequest) -> HttpResponse:
    """
    User authentication.
    :param request: client request
    :return: rendered page
    """
    if request.user.is_authenticated:
        return redirect(LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(LOGIN_REDIRECT_URL)
        else:
            messages.info(request, 'Username or password is incorrect.')

    return render(request, 'login/login.html')


def log_out(request: HttpRequest):
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)
