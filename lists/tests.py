from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from .models import Item
from lists.views import home_page

class TestForHomePage(TestCase):

    def test_root_url_resolves_the_home_page_view(self):

        self.assertEqual(resolve('/').func, home_page)

    def test_home_page_returns_correct_html(self):

        _response = self.client.get('/')
        self.assertTemplateUsed(_response, 'home.html')
    
    def test_can_save_a_POST_request(self):

        _response = self.client.post('/', data={'item_text':'A new item to add'})

        self.assertEqual(1, Item.objects.count())
        new_item_text = Item.objects.first()
        self.assertEqual('A new item to add', new_item_text.text)
    
    def test_redirects_after_POST(self):

        _response = self.client.post('/', data={'item_text':'A new item to add'})
        self.assertEqual(_response.status_code, 302)
        self.assertEqual(_response['location'], '/')

    def test_displays_multiple_lists(self):

        Item.objects.create(text='First Text')
        Item.objects.create(text='Second Text')

        _response = self.client.get('/')

        self.assertIn('First Text', _response.content.decode())
        self.assertIn('Second Text', _response.content.decode())

class TestItemModel(TestCase):
    
    def test_saving_and_retrieving_elements(self):

        first_item = Item()
        first_item.text = 'First ever item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(2, saved_items.count())

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1] 
        self.assertEqual(first_saved_item.text, 'First ever item')
        self.assertEqual(second_saved_item.text, 'Second item')