from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from posts.models import Post
from user.models import Subscriber
from user.tests.test_data import (TEST_POST_1, TEST_POST_2, TEST_POST_3,
                                  TEST_USER_1, TEST_USER_2, TEST_USER_3)

USER_MODEL = get_user_model()


class SubscriberModelTestCase(TestCase):
    test_user_1: User
    test_user_2: User
    test_user_3: User

    test_post_1: Post
    test_post_2: Post
    test_post_3: Post

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Create a users, their posts for further testing Subscriber model

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

    def setUp(self) -> None:
        self.subscriber_1 = Subscriber(user=self.test_user_1)
        self.subscriber_1.save()

    def test_subscriber_method(self) -> None:
        """
        Check addition of followed user (subscribe method)
        :return:
        """

        self.subscriber_1.subscribe(self.test_user_2)
        self.subscriber_1.subscribe(self.test_user_3)

        followed_user_1: User = self.subscriber_1.followed_users.get(username='test_2_username')
        followed_user_2: User = self.subscriber_1.followed_users.get(username='test_3_username')

        self.assertEqual(followed_user_1.username, self.test_user_2.username)
        self.assertEqual(followed_user_2.username, self.test_user_3.username)

    def test_unsubscriber_method(self):
        """
        Check deletion of followed user (unsubscribe method)
        :return:
        """
        self.subscriber_1.subscribe(self.test_user_2)
        self.subscriber_1.subscribe(self.test_user_3)

        followed_user_1: User = self.subscriber_1.followed_users.get(username='test_2_username')
        followed_user_2: User = self.subscriber_1.followed_users.get(username='test_3_username')

        self.assertEqual(followed_user_1.username, self.test_user_2.username)
        self.assertEqual(followed_user_2.username, self.test_user_3.username)

        self.subscriber_1.unsubscribe(self.test_user_2)
        self.subscriber_1.unsubscribe(self.test_user_3)

        self.assertRaises(USER_MODEL.DoesNotExist, self.subscriber_1.followed_users.get, username='test_2_username')
        self.assertRaises(USER_MODEL.DoesNotExist, self.subscriber_1.followed_users.get, username='test_3_username')

    def test_is_followed_user(self):
        """
        Check is_user_followed method
        :return:
        """
        self.subscriber_1.subscribe(self.test_user_2)

        self.assertTrue(self.subscriber_1.is_user_followed(self.test_user_2))
        self.assertFalse(self.subscriber_1.is_user_followed(self.test_user_3))

    def test_posts_followed_users(self):
        """
        Check user_posts method
        :return:
        """
        self.subscriber_1.subscribe(self.test_user_2)

        self.assertEqual(self.subscriber_1.user_posts[0].title, self.test_post_2.title)
        self.assertEqual(self.subscriber_1.user_posts[1].title, self.test_post_1.title)
