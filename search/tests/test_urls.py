from django.test import SimpleTestCase
from django.urls import resolve, reverse

from search.views import search


class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, search)
