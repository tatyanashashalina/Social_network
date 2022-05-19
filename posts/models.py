from django.contrib.auth import get_user_model
from django.db import models

USER_MODEL = get_user_model()


class PostManager(models.Manager):
    def valid_posts(self):
        return super().get_queryset().filter(hidden=False)


class Post(models.Model):
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name='owner')
    title = models.CharField(max_length=255, verbose_name='title')
    text_context = models.TextField(verbose_name='text context')
    image = models.ImageField(upload_to='posts_images/', null=True, blank=True, verbose_name='image')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='creation date')
    hidden = models.BooleanField(default=False, verbose_name='hidden')
    edited = models.BooleanField(default=False, verbose_name='edited')

    objects = PostManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-creation_date']

    def delete(self, using=None, keep_parents=False):
        self.hidden = True
        self.save()

    def __str__(self):
        return self.title
