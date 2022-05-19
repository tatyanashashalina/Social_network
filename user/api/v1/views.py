from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from posts.api.v1.serializers import PostSerializer
from posts.models import Post
from user.models import Subscriber

# todo: API authentication via tokens
# from .decorators import authentication_required
from .serializers import FeedSerializer, UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'], serializer_class=PostSerializer)
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

    # @authentication_required
    @action(detail=False, methods=['GET'], url_path='feed')
    def posts_feed(self, request: Request, pk: int = None) -> Response:
        """
        Collect posts from subscriptions
        :param request: client request
        :type request: Request
        :param pk: user primary key
        :type pk: int
        :return: Response
        """
        try:
            subscriptions = request.user.subscriptions
        except ObjectDoesNotExist:
            return Response({'message': 'Subscriber not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FeedSerializer(instance=subscriptions, context={'request': request})
        return Response(serializer.data)

    # @authentication_required
    @action(detail=True, methods=['POST'])
    def subscribe(self, request: Request, pk: int = None) -> Response:
        """
        Action to subscribe or unsubscribe user.
        :param request: client request
        :type request: Request
        :param pk: user primary key
        :type pk: int
        :return: Response
        """
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'message': 'Suggested user did not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user:
            return Response({'message': 'Can not follow self'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            subscriber, _ = Subscriber.objects.get_or_create(user=request.user, defaults={'user': request.user})
            if subscriber.is_user_followed(user):
                subscriber.unsubscribe(user)
                return Response({'message': 'unsubscribed'})
            subscriber.followed_users.add(user)
        return Response({'message': 'subscribed'})
