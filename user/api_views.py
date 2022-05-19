from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from posts.api.v1.serializers import PostSerializer
from posts.models import Post
from user.serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get', 'post'], serializer_class=PostSerializer)
    def posts(self, request: Request, pk: int = None) -> Response:
        """
        View of url "/users/{user_id/posts}". View handles both GET and POST requests.

        :param request: client request
        :type request: Request
        :param pk: the primary key of the user model, in the url it is user_id
        :type pk: int
        :return: Response
        """
        if not request.POST:
            user_posts = Post.objects.valid_posts().filter(owner=User.objects.get(id=pk)).order_by('-creation_date')
            data = PostSerializer(user_posts, many=True).data

            return Response(data=data)
