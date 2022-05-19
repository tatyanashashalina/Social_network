from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from config.settings import LOGIN_URL
from user.models import Subscriber

USER_MODEL = get_user_model()


@login_required(login_url=LOGIN_URL)
def search(request):
    subscriber, _ = Subscriber.objects.get_or_create(user=request.user, defaults={'user': request.user})
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q))
        data = USER_MODEL.objects.all().filter(multiple_q)
    else:
        data = USER_MODEL.objects.all()

    for user in data:
        user.is_user_followed = subscriber.is_user_followed(user)

    context = {
        'data': data
    }
    return render(request, 'search/index.html', context)
