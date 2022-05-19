from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# possible buttons of user actions
from config.settings import LOGIN_URL
from user.models import Subscriber

BUTTON_FOLLOW_TYPE, BUTTON_UNFOLLOW_TYPE, BUTTON_CREATE_POST_TYPE = range(3)
BUTTON_FOLLOW_LABEL, BUTTON_UNFOLLOW_LABEL, BUTTON_CREATE_POST_LABEL = "Follow", "Unfollow", "Create post"
BUTTON_BLANK_TYPE = -1
BUTTON_BLANK_LABEL = "BLANK"


@login_required(login_url=LOGIN_URL)
def profile(request: HttpRequest, user_id: int = None) -> HttpResponse | HttpResponseNotFound:
    """
    View of url "/profile/" and "/profile/<int:user_id>/" "

    :param request: request from client
    :type request: HttpRequest
    :param user_id: user_id if another user profile
    :return: rendered html page
    """
    user = request.user
    if user_id is not None:
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

    subscriber, _ = Subscriber.objects.get_or_create(user=request.user, defaults={'user': request.user})

    btn_type = BUTTON_BLANK_TYPE
    btn_label = BUTTON_BLANK_LABEL

    if request.user.id == user_id or user_id is None:
        btn_type = BUTTON_CREATE_POST_TYPE
        btn_label = BUTTON_CREATE_POST_LABEL

    elif subscriber.is_user_followed(user):
        # request.user follows another user
        btn_type = BUTTON_UNFOLLOW_TYPE
        btn_label = BUTTON_UNFOLLOW_LABEL

    else:
        # request.user doesn't follow another user
        btn_type = BUTTON_FOLLOW_TYPE
        btn_label = BUTTON_FOLLOW_LABEL

    context: dict = {
        'btn_type': btn_type,
        'btn_label': btn_label,
        'user': user,
        'is_other_profile': request.user.id != user.id,
    }

    return render(request, 'user/profile.html', context=context)


@login_required
def feed(request: HttpRequest) -> HttpResponse:
    return render(request, 'user/feed.html')
