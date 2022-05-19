from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.test import APITestCase

from posts.models import Post
from user.tests.test_data import (TEST_POST_1, TEST_POST_2, TEST_USER_1,
                                  TEST_USER_2)


class PostDestroyTestCase(APITestCase):
    test_user_1: User
    test_user_2: User

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Create a users for further testing API views

        :return: None
        """
        cls.test_user_1: User = User.objects.create_user(**TEST_USER_1)
        cls.test_user_2: User = User.objects.create_user(**TEST_USER_2)

        cls.test_user_1.save()
        cls.test_user_2.save()

    def setUp(self) -> None:
        """
        Create posts for further testing API views

        :return: None
        """
        TEST_POST_1['owner']: User = self.test_user_1
        TEST_POST_2['owner']: User = self.test_user_2

        self.test_post_1: Post = Post.objects.create(**TEST_POST_1)
        self.test_post_2: Post = Post.objects.create(**TEST_POST_2)

        self.test_post_1.save()
        self.test_post_2.save()

        self.delete_test_post_1_url = f'/api/v1/posts/{self.test_post_1.id}/destroy/'
        self.delete_test_post_2_url = f'/api/v1/posts/{self.test_post_2.id}/destroy/'
        self.delete_not_exist_post_url = '/api/v1/posts/-1/destroy/'

    def test_deletion_post(self) -> None:
        """
        Check that deleted post will have "hidden" field equal True

        :return:
        """
        initial_number_of_valid_posts: int = Post.objects.valid_posts().count()

        logged: bool = self.client.login(username=self.test_user_1.username, password=TEST_USER_1['password'])
        self.assertTrue(logged)

        response: Response = self.client.delete(self.delete_test_post_1_url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.valid_posts().count(), initial_number_of_valid_posts - 1)
        self.assertTrue(Post.objects.get(id=self.test_post_1.id).hidden)

    def test_deletion_post_of_another_user(self) -> None:
        """
        Check the API will not allow you to delete another user's post
        :return:
        """
        initial_number_of_valid_posts: int = Post.objects.valid_posts().count()

        logged: bool = self.client.login(username=self.test_user_1.username, password=TEST_USER_1['password'])
        self.assertTrue(logged)

        response: Response = self.client.delete(self.delete_test_post_2_url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Post.objects.valid_posts().count(), initial_number_of_valid_posts)
        self.assertFalse(Post.objects.get(id=self.test_post_1.id).hidden)

    def test_deletion_not_exist_post(self) -> None:
        """
        Check the API return Not Found Response if to delete not exist post
        :return: None
        """
        logged: bool = self.client.login(username=self.test_user_1.username, password=TEST_USER_1['password'])
        self.assertTrue(logged)

        response: Response = self.client.delete(self.delete_not_exist_post_url)
        self.assertEqual(response.status_code, 404)
