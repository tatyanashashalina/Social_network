from django.urls import path

from .views import PostDestroy

urlpatterns = [
    path('posts/<int:id>/destroy/', PostDestroy.as_view()),
]
