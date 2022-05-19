from rest_framework.views import Response
from rest_framework import status

from functools import wraps


def authentication_required(func):
    """
    Verify user authentication for use API
    """
    @wraps(func)
    def wrapper(view, request, *args, **kwargs):
        if request.user.is_authenticated:
            result = func(view, request, *args, **kwargs)
            return result
        return Response('Not authorized', status=status.HTTP_403_FORBIDDEN)
    return wrapper
