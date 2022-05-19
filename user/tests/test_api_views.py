from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.test import APITestCase

from posts.models import Post
from user.models import Subscriber
from user.tests.test_data import (TEST_POST_1, TEST_POST_2, TEST_POST_3,
                                  TEST_USER_1, TEST_USER_2, TEST_USER_3)

USER_MODEL = get_user_model()


class UserViewSetTestCase(APITestCase):
    test_user_1: User
    test_user_2: User

    @classmethod
    def setUpTestData(cls):
        """
        Create a users for further testing API views

        :return: None
        """
        cls.test_user_1: User = USER_MODEL.objects.create_user(**TEST_USER_1)
        cls.test_user_2: User = USER_MODEL.objects.create_user(**TEST_USER_2)
        cls.test_user_1.save()
        cls.test_user_2.save()

        cls.url_users_list: str = '/api/v1/users/'
        cls.url_test_user_1_detail: str = f'/api/v1/users/{cls.test_user_1.id}/'

    def test_user_list(self):
        """
        Test to get user list using API

        :return: None
        """
        response: Response = self.client.get(self.url_users_list, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_user_detail(self):
        """
        Test to get detail user using API and check content of fields.

        :return: None
        """
        response: Response = self.client.get(self.url_test_user_1_detail, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['id'], self.test_user_1.id)
        self.assertEqual(response.data['username'], self.test_user_1.username)
        self.assertEqual(response.data['email'], self.test_user_1.email)
        self.assertEqual(response.data['first_name'], self.test_user_1.first_name)
        self.assertEqual(response.data['last_name'], self.test_user_1.last_name)


class PostViewSetTestCase(APITestCase):
    test_user_1: User
    test_user_2: User

    test_post_1: Post
    test_post_2: Post

    @classmethod
    def setUpTestData(cls):
        """
        Create a users, their posts for further testing API views

        :return: None
        """
        cls.test_user_1: User = USER_MODEL.objects.create_user(**TEST_USER_1)
        cls.test_user_2: User = USER_MODEL.objects.create_user(**TEST_USER_2)

        cls.test_user_1.save()
        cls.test_user_2.save()

        TEST_POST_1['owner']: User = cls.test_user_1
        TEST_POST_2['owner']: User = cls.test_user_1

        cls.test_post_1: Post = Post.objects.create(**TEST_POST_1)
        cls.test_post_2: Post = Post.objects.create(**TEST_POST_2)

        cls.test_post_1.save()
        cls.test_post_2.save()

        cls.url_get_posts_of_test_user_1: str = f'/api/v1/users/{cls.test_user_1.id}/posts/'

    def test_list_of_posts_of_one_user(self):
        """
        Test to get posts of user

        :return: None
        """
        response: Response = self.client.get(self.url_get_posts_of_test_user_1, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_sorting_list_of_posts_of_user(self):
        """
        Check sorting of list of posts of the user

        :return: None
        """
        response: Response = self.client.get(self.url_get_posts_of_test_user_1, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], self.test_post_2.id)


class SubscribeAPITestCase(APITestCase):
    test_user_1: User
    test_user_2: User

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Create a users, their posts for further testing Subscribe API

        :return: None
        """
        cls.test_user_1 = USER_MODEL.objects.create_user(**TEST_USER_1)
        cls.test_user_2 = USER_MODEL.objects.create_user(**TEST_USER_2)
        cls.test_user_1.save()
        cls.test_user_2.save()

        cls.url_subscribe2test_user_1 = f'/api/v1/users/{cls.test_user_1.id}/subscribe/'
        cls.url_subscribe2test_user_2 = f'/api/v1/users/{cls.test_user_2.id}/subscribe/'

        cls.url_subscribe2non_existent_user = '/api/v1/users/10002/subscribe/'

    def test_subscribe_method_via_API(self) -> None:
        """
        Check the subscribe method of the Subscriber model via API
        :return: None
        """
        self.client.login(username=self.test_user_1, password=TEST_USER_1['password'])

        response: Response = self.client.post(self.url_subscribe2test_user_2)
        self.assertEqual(response.status_code, 200)

        # subscribe
        subscriber_test_user_1: Subscriber = Subscriber.objects.get(user=self.test_user_1)
        self.assertTrue(subscriber_test_user_1.is_user_followed(self.test_user_2))

    def test_unsubscribe_method_via_API(self) -> None:
        """
        Check the unsubscribe method of the Subscriber model via API
        :return: None
        """
        self.client.login(username=self.test_user_1, password=TEST_USER_1['password'])

        # subscribe
        response_1: Response = self.client.post(self.url_subscribe2test_user_2)
        self.assertEqual(response_1.status_code, 200)

        subscriber_test_user_1: Subscriber = Subscriber.objects.get(user=self.test_user_1)
        self.assertTrue(subscriber_test_user_1.is_user_followed(self.test_user_2))

        # unsubscribe
        response_2: Response = self.client.post(self.url_subscribe2test_user_2)
        self.assertEqual(response_2.status_code, 200)

        self.assertFalse(subscriber_test_user_1.is_user_followed(self.test_user_2))

    def test_subscribe2non_existent_user(self):
        """
        Checking to return an error about subscribing to a non-existent user (404 status code)
        :return:
        """
        self.client.login(username=self.test_user_1, password=TEST_USER_1['password'])

        response: Response = self.client.post(self.url_subscribe2non_existent_user)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Suggested user did not found')

    def test_subscribe2self(self):
        self.client.login(username=self.test_user_1, password=TEST_USER_1['password'])

        response: Response = self.client.post(self.url_subscribe2test_user_1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Can not follow self')


class FeedAPITestCase(APITestCase):
    test_user_1: User
    test_user_2: User
    test_user_3: User

    test_post_1: Post
    test_post_2: Post
    test_post_3: Post

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Create a users, their posts for further testing to get feed via API

        :return: None
        """
        cls.test_user_1 = USER_MODEL.objects.create_user(**TEST_USER_1)
        cls.test_user_2 = USER_MODEL.objects.create_user(**TEST_USER_2)
        cls.test_user_3 = USER_MODEL.objects.create_user(**TEST_USER_3)
        cls.test_user_1.save()
        cls.test_user_2.save()
        cls.test_user_3.save()

        TEST_POST_1['owner'] = cls.test_user_2
        TEST_POST_2['owner'] = cls.test_user_2
        TEST_POST_3['owner'] = cls.test_user_3

        cls.test_post_1 = Post.objects.create(**TEST_POST_1)
        cls.test_post_2 = Post.objects.create(**TEST_POST_2)
        cls.test_post_3 = Post.objects.create(**TEST_POST_3)

        cls.test_post_1.save()
        cls.test_post_2.save()
        cls.test_post_3.save()

        cls.url_get_feed = '/api/v1/users/feed/'

    def setUp(self) -> None:
        self.subscriber_1 = Subscriber(user=self.test_user_1)
        self.subscriber_1.save()

    def test_get_user_feed(self):
        """
        Checking to get the user feed
        :return: Тщту
        """
        self.subscriber_1.subscribe(self.test_user_2)
        self.subscriber_1.subscribe(self.test_user_3)

        self.client.login(username=self.test_user_1, password=TEST_USER_1['password'])

        response: Response = self.client.get(self.url_get_feed)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['followed_user_posts']), 3)

    def test_get_empty_user_feed(self):
        """
        Checking to get the empty user feed
        :return:
        """
        self.client.login(username=self.test_user_1, password=TEST_USER_1['password'])

        response: Response = self.client.get(self.url_get_feed)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['followed_user_posts']), 0)
