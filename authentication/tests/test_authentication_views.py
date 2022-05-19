from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

USER_MODEL = get_user_model()


class UserLoginViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.existing_user = USER_MODEL.objects.create(
            username='existing_username',
            password='psswrd09'
        )
        cls.existing_user.save()
        cls.url = '/login/'

    def setUp(self) -> None:
        self.some_user: dict = {
            'username': 'some_username',
            'password': 'psswrd010'
        }

    def test_login(self):
        """
        Test log in of user.
        :return:
        """
        username = 'some_username'
        password = 'psswrd010'
        user = USER_MODEL.objects.create_user(username=username,
                                              password=password)
        user.save()
        response = self.client.post(reverse('login'),
                                    {'username': username,
                                     'password': password},
                                    follow=True)

        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_user_get_page(self) -> None:
        """
        Test authentication of user view by GET method.
        :return:
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html', 'base.html')

    def test_login_user_with_correct_data(self) -> None:
        """
        Test authentication of user view with correct data.
        :return:
        """
        data = {
            'username': 'existing_username',
            'password': 'psswrd09'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html', 'base.html')

        saved_user = USER_MODEL.objects.get(username='existing_username')

        self.assertEqual(saved_user.username, 'existing_username')

    def test_login_user_with_incorrect_data(self) -> None:
        """
        Test authentication of user view with incorrect data.
        :return:
        """
        response = self.client.post(self.url, self.some_user)

        self.assertEqual(response.status_code, 200)
        self.assertRaises(USER_MODEL.DoesNotExist, USER_MODEL.objects.get, username='some_username')
