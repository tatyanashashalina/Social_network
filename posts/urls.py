from django.urls import path
from .views import NewPostView
from .views import PostEditView

from .views import NewPostView


app_name = 'posts'

urlpatterns = [
    path('new/', NewPostView.as_view(), name='new'),
    path('edit/<int:post_id>/', PostEditView.as_view(), name='post-edit')
]
