from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as l_

user_model = get_user_model()


class Subscriber(models.Model):
    """
    User subscriber model.
    Uses to get information from subscriptions entity.
    """
    user = models.OneToOneField(user_model, on_delete=models.CASCADE, related_name='subscriptions')
    followed_users = models.ManyToManyField(user_model, verbose_name=l_('Subscriptions'))

    class Meta:
        verbose_name = l_('Subscriber')
        verbose_name_plural = l_('Subscribers')

    def __str__(self):
        return f"{self.user.username} subscriptions"

    @property
    def user_posts(self) -> list:
        """
        Collect posts from followed users
        :return: list
        """
        queryset = self.followed_users.prefetch_related('posts')
        posts = [post for user in queryset.all() for post in user.posts.filter(hidden=False)]
        return posts

    def subscribe(self, user):
        """
        Follow user posts
        """
        self.followed_users.add(user)

    def unsubscribe(self, user):
        """
        Unfollow user posts
        :param user: user instance
        """
        self.followed_users.remove(user)

    def is_user_followed(self, user) -> bool:
        """
        Verify that user follows suggested user
        :param user: user instance
        :return: bool
        """
        return self.followed_users.filter(pk=user.pk).exists()
