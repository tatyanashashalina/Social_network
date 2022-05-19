from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import DestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from posts.models import Post


class PostDestroy(DestroyAPIView):
    queryset = Post.objects.valid_posts()
    lookup_field = 'id'

    def delete(self, request: Request, *args, **kwargs) -> Response:
        post_id: int = kwargs.get('id', -1)
        try:
            post: Post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            return Response(status=404)

        if post.owner.id == request.user.id:
            return super().delete(request, *args, **kwargs)
        else:
            return Response(status=401)
