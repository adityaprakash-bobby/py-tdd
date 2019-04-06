from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

# Create your tests here.
# class ThisWillFailTesting(TestCase):

#     def test_bad_at_maths(self):

#         self.assertEqual(1 + 1, 3)

class TestForHomePage(TestCase):

    def test_root_url_resolves_the_home_page_view(self):

        self.assertEqual(resolve('/').func, home_page)