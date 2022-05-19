from django.contrib.auth import get_user_model
from django.test import TestCase

from registration.forms import EXISTING_EMAIL_ERROR_MESSAGE

USER_MODEL = get_user_model()


class UserRegistrationFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.some_user = USER_MODEL.objects.create(
            username='existing_username',
            email='existing_email@gmail.com',
            first_name='existing_user_first_name',
            last_name='existing_user_last_name',
            password='zxcvbnm1234'
        )
        cls.some_user.save()

        cls.url = '/register/'

    def setUp(self) -> None:
        self.new_user: dict = {
            'username': 'new_user_username',
            'email': 'new_user_email@gmail.com',
            'first_name': 'new_user_first_name',
            'last_name': 'new_user_last_name',
            'password1': 'zxcvbnm1234',
            'password2': 'zxcvbnm1234',
        }

    def test_register_user_get_page(self) -> None:
        """
            Test registration of user view by GET method.

            :return:
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_user_with_correct_data(self) -> None:
        """
        Test registration of user view with correct data.

        :return:
        """

        response = self.client.post(self.url, self.new_user, follow=True)
        # redirect to 'login'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')

        saved_user = USER_MODEL.objects.get(username='new_user_username')

        self.assertEqual(saved_user.first_name, 'new_user_first_name')

    def test_register_user_with_incorrect_email(self) -> None:
        """
        Test registration of user view with incorrect email.

        :return:
        """

        self.new_user['email'] = 'new_user_email.com'

        response = self.client.post(self.url, self.new_user)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'email', 'Enter a valid email address.')

        self.assertRaises(USER_MODEL.DoesNotExist, USER_MODEL.objects.get, username='new_user_username')

    def test_register_user_with_existing_email(self) -> None:
        """
        Test registration of user view with existing email.

        :return:
        """

        self.new_user['email'] = 'existing_email@gmail.com'

        response = self.client.post(self.url, self.new_user)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'email', EXISTING_EMAIL_ERROR_MESSAGE)

        self.assertRaises(USER_MODEL.DoesNotExist, USER_MODEL.objects.get, username='new_user_username')

    def test_register_user_with_existing_username(self) -> None:
        """
        Test registration of user view with existing username.

        :return:
        """

        self.new_user['username'] = 'existing_username'

        response = self.client.post(self.url, self.new_user)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'username', 'A user with that username already exists.')

        self.assertRaises(USER_MODEL.DoesNotExist, USER_MODEL.objects.get, email='new_user_email@gmail.com')

    def test_register_user_with_small_password(self) -> None:
        """
        Test registration of user view with small password.

        :return:
        """

        self.new_user['password1'] = 'sap'
        self.new_user['password2'] = 'sap'

        response = self.client.post(self.url, self.new_user)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'user_form',
            'password2',
            'This password is too short. It must contain at least 8 characters.'
        )

        self.assertRaises(USER_MODEL.DoesNotExist, USER_MODEL.objects.get, username='new_user_username')

    def test_register_user_with_mismatched_passwords(self) -> None:
        """
        Test registration of user view with mismatched passwords.

        :return:
        """

        self.new_user['password1'] = 'zxcvbnm12'
        self.new_user['password2'] = 'zxcvbnm1234'

        response = self.client.post(self.url, self.new_user)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'password2', 'The two password fields didn’t match.')

        self.assertRaises(USER_MODEL.DoesNotExist, USER_MODEL.objects.get, username='new_user_username')

    def test_register_user_without_password(self) -> None:
        """
        Test registration of user view without password.

        :return:
        """

        self.new_user['password1'] = ''
        self.new_user['password2'] = ''

        response = self.client.post(self.url, self.new_user)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'password1', 'This field is required.')
        self.assertFormError(response, 'user_form', 'password2', 'This field is required.')

        self.assertRaises(USER_MODEL.DoesNotExist, USER_MODEL.objects.get, username='new_user_username')

    def test_register_user_without_username(self) -> None:
        """
        Test registration of user view without username.

        :return:
        """

        self.new_user['username'] = ''

        response = self.client.post(self.url, self.new_user)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'username', 'This field is required.')

        self.assertRaises(USER_MODEL.DoesNotExist, USER_MODEL.objects.get, email='new_user_email@gmail.com')

    def test_register_user_without_email(self) -> None:
        """
        Test registration of user view without email.

        :return:
        """

        self.new_user['email'] = ''

        response = self.client.post(self.url, self.new_user)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'email', 'This field is required.')

        self.assertRaises(USER_MODEL.DoesNotExist, USER_MODEL.objects.get, username='new_user_username')
