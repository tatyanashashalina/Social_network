# from django.urls import path
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import SimpleRouter

from user.api.v1.views import UserViewSet

router = SimpleRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    # path('login/', ObtainAuthToken.as_view())
] + router.urls
