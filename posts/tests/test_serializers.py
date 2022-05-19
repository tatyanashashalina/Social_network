from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from posts.api.v1.serializers import PostSerializer
from posts.models import Post


class PostSerializerTestCase(APITestCase):
    test_user: User
    test_post: Post

    @classmethod
    def setUpTestData(cls):
        """
        Creating a user, his post, initializing an instance of the serializer for further testing.
        :return: None
        """
        cls.test_user: User = User.objects.create_user(
            username='test_username',
            email='test_email@gmail.com',
            password='zxcvbnm1234',
            first_name='test_firstname',
            last_name='test_lastname'
        )
        cls.test_user.save()

        cls.test_post: Post = Post.objects.create(
            title="Test title",
            text_context="Some text",
            image=None,
            owner=cls.test_user
        )
        cls.test_post.save()

        cls.serializer: PostSerializer = PostSerializer(cls.test_post)

    def test_contain_expected_fields(self):
        """
        Checking the expected keys in the data
        :return: None
        """
        self.assertCountEqual(self.serializer.data.keys(), ['id', 'title', 'text_context', 'image', 'creation_date',
                                                            'edited'])

    def test_correct_values(self):
        """
        Checking the content of the expected fields.
        :return: None
        """
        self.assertEqual(self.serializer.data['title'], self.test_post.title)
        self.assertEqual(self.serializer.data['text_context'], self.test_post.text_context)
        self.assertEqual(self.serializer.data['image'], self.test_post.image)
