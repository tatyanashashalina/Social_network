from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .models import Post


class NewPostView(CreateView):
    model = Post
    template_name = 'posts/new.html'
    fields = ['title', 'text_context', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NewPostView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text_context', 'image']
    template_name = 'posts/post_edit.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):

        post = self.get_object(self.queryset)
        post.edited = True
        post.save()
        return reverse_lazy('profile')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner
