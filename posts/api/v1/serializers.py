from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostSerializer(ModelSerializer):
    """
    Post Serializer
    """
    class Meta:
        model = Post
        fields = ['id', 'title', 'text_context', 'image', 'creation_date', 'edited']
