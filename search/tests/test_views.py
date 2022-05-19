from django.test import TestCase
from django.urls import reverse

from search.views import USER_MODEL


class TestViews(TestCase):
    def setUp(self):
        self.list_url = reverse('search')

        self.test_user_1 = USER_MODEL.objects.create_user(
            username='TestUser1',
            email='test_user1@gmail.com',
            first_name='Test',
            last_name='User1',
            password='TestPassword'
        )

        self.test_user_2 = USER_MODEL.objects.create_user(
            username='TestUser2',
            email='test_user2@gmail.com',
            first_name='Test',
            last_name='User2',
            password='TestPassword'
        )

        self.test_user_1.save()
        self.test_user_2.save()

    def test_project_list_GET(self):
        self.client.login(username='TestUser2', password='TestPassword')

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/index.html')

    def test_search_user(self):
        self.client.login(username='TestUser2', password='TestPassword')

        response = self.client.get(reverse("search"), {"q": "TestUser1"})
        result = response.context['data']
        self.assertQuerysetEqual(list(USER_MODEL.objects.filter(username="TestUser1")), result)

    def test_search_all_users(self):
        self.client.login(username='TestUser2', password='TestPassword')

        response = self.client.get(reverse("search"), {"q": ""})
        result = response.context['data']
        self.assertQuerysetEqual(list(USER_MODEL.objects.all()), result)
