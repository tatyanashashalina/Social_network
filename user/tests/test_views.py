from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase

from posts.models import Post
from user.tests.test_data import (TEST_POST_1, TEST_POST_2, TEST_USER_1,
                                  TEST_USER_2)
from user.views import BUTTON_CREATE_POST_LABEL, BUTTON_CREATE_POST_TYPE


class ProfileViewTestCase(TestCase):
    test_user_1: User
    test_user_2: User

    test_post_1: Post
    test_post_2: Post

    @classmethod
    def setUpTestData(cls):
        """
        Create a users, their posts for further testing views

        :return: None
        """
        cls.test_user_1: User = User.objects.create_user(**TEST_USER_1)
        cls.test_user_2: User = User.objects.create_user(**TEST_USER_2)
        cls.test_user_1.save()
        cls.test_user_2.save()

        TEST_POST_1['owner']: User = cls.test_user_1
        TEST_POST_2['owner']: User = cls.test_user_1

        cls.test_post_1: Post = Post.objects.create(**TEST_POST_1)
        cls.test_post_2: Post = Post.objects.create(**TEST_POST_2)

        cls.test_post_1.save()
        cls.test_post_2.save()

        cls.profile_url: str = '/profile/'
        cls.profile_another_user_url: str = f'/profile/{cls.test_user_1.id}/'

    def test_redirect_for_not_logged_user(self) -> None:
        """
        Checking redirects to the login of a not logged user
        :return: None
        """
        response_profile: HttpResponse = self.client.get(self.profile_url, follow=True)

        self.assertEqual(response_profile.status_code, 200)
        self.assertTemplateUsed(response_profile, 'login/login.html')

        response_another_user_profile: HttpResponse = self.client.get(self.profile_another_user_url, follow=True)

        self.assertEqual(response_another_user_profile.status_code, 200)
        self.assertTemplateUsed(response_another_user_profile, 'login/login.html')

    def test_get_profile_page(self) -> None:
        """
        Testing the user profile page
        :return: None
        """
        logged: bool = self.client.login(username=self.test_user_1.username, password=TEST_USER_1['password'])
        self.assertTrue(logged)

        response: HttpResponse = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

        self.assertEqual(response.context['user'].id, self.test_user_1.id)
        self.assertEqual(response.context['user'].username, self.test_user_1.username)
        self.assertEqual(response.context['btn_label'], BUTTON_CREATE_POST_LABEL)
        self.assertEqual(response.context['btn_type'], BUTTON_CREATE_POST_TYPE)
        self.assertFalse(response.context['is_other_profile'])

        self.assertContains(response, self.test_user_1.username)

    def test_get_profile_page_via_id(self) -> None:
        """
        Testing the user profile page via id
        :return: None
        """
        logged: bool = self.client.login(username=self.test_user_1.username, password=TEST_USER_1['password'])
        self.assertTrue(logged)

        response: HttpResponse = self.client.get(self.profile_another_user_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

        self.assertEqual(response.context['user'].id, self.test_user_1.id)
        self.assertEqual(response.context['user'].username, self.test_user_1.username)
        self.assertEqual(response.context['btn_label'], BUTTON_CREATE_POST_LABEL)
        self.assertEqual(response.context['btn_type'], BUTTON_CREATE_POST_TYPE)
        self.assertFalse(response.context['is_other_profile'])

        self.assertContains(response, self.test_user_1.username)

    def test_get_profile_of_another_user(self) -> None:
        """
        Testing for another user's profile page
        :return:
        """
        logged: bool = self.client.login(username=self.test_user_2.username, password=TEST_USER_2['password'])
        self.assertTrue(logged)

        response: HttpResponse = self.client.get(self.profile_another_user_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

        self.assertEqual(response.context['user'].id, self.test_user_1.id)
        self.assertEqual(response.context['user'].username, self.test_user_1.username)
        self.assertTrue(response.context['is_other_profile'])

        self.assertContains(response, self.test_user_1.username)
