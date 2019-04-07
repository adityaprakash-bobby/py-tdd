from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class TestForHomePage(TestCase):

    def test_root_url_resolves_the_home_page_view(self):

        self.assertEqual(resolve('/').func, home_page)

    def test_home_page_returns_correct_html(self):

        _response = self.client.get('/')
        self.assertTemplateUsed(_response, 'home.html')
    
    def test_can_save_a_POST_request(self):

        _response = self.client.post('/', data={'item_text':'A new item to add'})
        self.assertIn('A new item to add',_response.content.decode('utf-8'))
        self.assertTemplateUsed(_response, 'home.html')
