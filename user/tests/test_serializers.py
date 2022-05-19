from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from user.api.v1.serializers import UserSerializer
from user.tests.test_data import TEST_USER_1


class UserSerializerTestCase(APITestCase):
    test_user: User

    @classmethod
    def setUpTestData(cls):
        """
        Creating a user, initializing an instance of the serializer for further testing.

        :return: None
        """
        cls.test_user: User = User.objects.create_user(**TEST_USER_1)
        cls.test_user.save()

        cls.serializer: UserSerializer = UserSerializer(cls.test_user)

    def test_contain_expected_fields(self):
        """
        Checking the expected keys in the data

        :return: None
        """
        self.assertCountEqual(self.serializer.data.keys(), ['id', 'username', 'email', 'first_name', 'last_name'])

    def test_correct_values(self):
        """
        Checking the content of the expected fields.

        :return: None
        """
        self.assertEqual(self.serializer.data['username'], self.test_user.username)
        self.assertEqual(self.serializer.data['email'], self.test_user.email)
        self.assertEqual(self.serializer.data['first_name'], self.test_user.first_name)
        self.assertEqual(self.serializer.data['last_name'], self.test_user.last_name)
