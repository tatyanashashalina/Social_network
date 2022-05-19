from django.contrib.auth import get_user_model
from django.test import TestCase

from registration.forms import UserRegistrationForm

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

    def setUp(self) -> None:
        self.new_user: dict = {
            'username': 'new_user_username',
            'email': 'new_user_email@gmail.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password1': 'zxcvbnm1234',
            'password2': 'zxcvbnm1234',
        }

    def test_register_user_with_correct_data(self) -> None:
        """
        Test registration of user with correct data.

        :return:
        """

        form = UserRegistrationForm(self.new_user)
        self.assertTrue(form.is_valid())

    def test_register_user_with_incorrect_email(self) -> None:
        """
        Test registration of user with incorrect email.

        :return:
        """

        self.new_user['email'] = 'new_user_email.com'

        form = UserRegistrationForm(self.new_user)
        self.assertFalse(form.is_valid())

    def test_register_user_with_existing_email(self) -> None:
        """
        Test registration of user with existing email.

        :return:
        """

        self.new_user['email'] = 'existing_email@gmail.com'

        form = UserRegistrationForm(self.new_user)
        self.assertFalse(form.is_valid())

    def test_register_user_with_existing_username(self) -> None:
        """
        Test registration of user with existing username.

        :return:
        """

        self.new_user['username'] = 'existing_username'

        form = UserRegistrationForm(self.new_user)
        self.assertFalse(form.is_valid())

    def test_register_user_with_small_password(self) -> None:
        """
        Test registration of user with small password.

        :return:
        """

        self.new_user['password1'] = 'sap'
        self.new_user['password2'] = 'sap'

        form = UserRegistrationForm(self.new_user)
        self.assertFalse(form.is_valid())

    def test_register_user_with_mismatched_passwords(self) -> None:
        """
        Test registration of user with mismatched passwords.

        :return:
        """

        self.new_user['password1'] = 'zxcvbnm12'
        self.new_user['password2'] = 'zxcvbnm1234'

        form = UserRegistrationForm(self.new_user)
        self.assertFalse(form.is_valid())

    def test_register_user_without_password(self) -> None:
        """
        Test registration of user without password.

        :return:
        """

        self.new_user['password1'] = ''
        self.new_user['password2'] = ''

        form = UserRegistrationForm(self.new_user)
        self.assertFalse(form.is_valid())

    def test_register_user_without_username(self) -> None:
        """
        Test registration of user without username.

        :return:
        """

        self.new_user['username'] = ''

        form = UserRegistrationForm(self.new_user)
        self.assertFalse(form.is_valid())

    def test_register_user_without_email(self) -> None:
        """
        Test registration of user without email.

        :return:
        """

        self.new_user['email'] = ''

        form = UserRegistrationForm(self.new_user)
        self.assertFalse(form.is_valid())
