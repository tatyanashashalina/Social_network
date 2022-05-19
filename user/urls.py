from django.urls import path

from user.views import feed, profile

urlpatterns = [
    path('', profile, name='profile'),
    path('<int:user_id>/', profile, name='other_profile'),
    path('feed/', feed, name='news_feed')
]
