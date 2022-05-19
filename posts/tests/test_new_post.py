from django.test import TestCase, override_settings
from django.urls import reverse
from search.views import USER_MODEL
from django.core.files import File
from PIL import Image
from io import BytesIO
import shutil, tempfile

from posts.models import Post

MEDIA_ROOT = tempfile.mkdtemp()


def get_image_file(name, ext='png', size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class PostViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('posts:new')
        self.user = USER_MODEL.objects.create_user(username='test_user',
                                                   first_name='test_first_name',
                                                   last_name='test_last_name',
                                                   password='test_password')
        self.user.save()
        self.client.login(username='test_user', password='test_password')

        test_image = get_image_file('file1.png')

        self.post = Post.objects.create(title='test_title',
                                        text_context='test_text',
                                        image=test_image,
                                        owner=self.user)

    def test_new_post(self):
        new_image = get_image_file('file2.png')
        response = self.client.post(reverse('posts:new'),
                                    {'title': 'new_title', 'text_context': 'new_text', 'image': new_image})

        self.assertEqual(response.status_code, 302)

        new_post = Post.objects.get(title='new_title')

        self.assertEqual(new_post.title, 'new_title')
        self.assertEqual(new_post.text_context, 'new_text')
        self.assertIn(str(new_image.name)[:5], str(new_post.image))

    def test_templates_edit_post(self):
        response = self.client.get(reverse('posts:new'))
        self.assertTemplateUsed(response, 'posts/new.html')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
