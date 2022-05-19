from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from posts.api.v1.serializers import PostSerializer
from user.models import Subscriber


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class FeedPostOwnerSerializer(UserSerializer):
    """
    Serializer for get information about post owner
    """
    class Meta(UserSerializer.Meta):
        fields = ['id', 'username']


class FeedPostSerializer(PostSerializer):
    """
    Represents post for API
    """
    owner = FeedPostOwnerSerializer(many=False, read_only=True)
    creation_date = serializers.SerializerMethodField(method_name='format_creation_date')

    class Meta(PostSerializer.Meta):
        fields = ['id', 'title', 'text_context', 'image', 'creation_date', 'owner']

    def format_creation_date(self, instance):
        return instance.creation_date.strftime("%d-%m-%Y %H:%M:%S")


class FeedSerializer(serializers.ModelSerializer):
    """
    News feed serializer
    """

    followed_user_posts = serializers.SerializerMethodField()

    class Meta:
        model = Subscriber
        fields = ['followed_user_posts']

    def get_followed_user_posts(self, instance):
        try:
            posts = instance.user_posts
            serializer = FeedPostSerializer(posts, many=True, context=self.context)
            return serializer.data
        except ObjectDoesNotExist:
            return []
