from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from .models import Item, List
from lists.views import home_page

class TestForHomePage(TestCase):

    def test_root_url_resolves_the_home_page_view(self):

        self.assertEqual(resolve('/').func, home_page)

    def test_home_page_returns_correct_html(self):

        _response = self.client.get('/')
        self.assertTemplateUsed(_response, 'home.html')

class TestItemAndListModels(TestCase):
    
    def test_saving_and_retrieving_elements(self):
        
        list_ob = List()
        list_ob.save()

        first_item = Item()
        first_item.text = 'First ever item'
        first_item.list = list_ob
        first_item.save()

        second_item = Item()
        second_item.text = 'Second item'
        second_item.list = list_ob
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_ob)

        saved_items = Item.objects.all()
        self.assertEqual(2, saved_items.count())

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1] 
        self.assertEqual(first_saved_item.text, 'First ever item')
        self.assertEqual(first_saved_item.list, list_ob)
        self.assertEqual(second_saved_item.text, 'Second item')
        self.assertEqual(second_saved_item.list, list_ob)

class ListViewTest(TestCase):

    def test_uses_list_template(self):

        _response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(_response, 'list.html')

    def test_displays_all_items(self):
        
        list_ob = List.objects.create()
        Item.objects.create(text='First Item', list=list_ob)
        Item.objects.create(text='Second Item', list=list_ob)

        _response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(_response, 'First Item')
        self.assertContains(_response, 'Second Item')

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):

        self.client.post('/lists/new', data={'item_text':'A new item to add'})
        self.assertEqual(1, Item.objects.count())
        new_item = Item.objects.first()
        self.assertEqual('A new item to add', new_item.text)

    def test_redirects_after_POST(self):

        _response = self.client.post('/lists/new', data={'item_text':'A new item to add'})
        self.assertRedirects(_response, '/lists/the-only-list-in-the-world/') 