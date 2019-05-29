from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from lists.models import Item, List
from lists.views import home_page

class TestForHomePage(TestCase):

    def test_root_url_resolves_the_home_page_view(self):

        self.assertEqual(resolve('/').func, home_page)

    def test_home_page_returns_correct_html(self):

        _response = self.client.get('/')
        self.assertTemplateUsed(_response, 'home.html')

class ListViewTest(TestCase):

    def test_uses_list_template(self):

        list_ob = List.objects.create()
        _response = self.client.get(f'/lists/{list_ob.id}/')
        self.assertTemplateUsed(_response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        
        correct_list = List.objects.create()
        Item.objects.create(text='First Item', list=correct_list)
        Item.objects.create(text='Second Item', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='Other First Item', list=other_list)
        Item.objects.create(text='Other second Item', list=other_list)
        
        _response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(_response, 'First Item')
        self.assertContains(_response, 'Second Item')
        self.assertNotContains(_response, 'Other First Item')
        self.assertNotContains(_response, 'Other Second Item')

    def test_passes_correct_list_to_template(self):
        
        other_list = List.objects.create()
        correct_list = List.objects.create()

        _response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertEqual(_response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/', 
            data={'item_text':'A new item to add to existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item to add to existing list')
        self.assertEqual(correct_list, new_item.list)

    def test_POST_redirects_to_list_view(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        _response = self.client.post(f'/lists/{correct_list.id}/', 
            data={'item_text':'A new item to add to existing list'}
        )

        self.assertRedirects(_response, f'/lists/{correct_list.id}/')

    def test_validation_error_ends_up_in_list_view(self):

        list_ob = List.objects.create()

        _response = self.client.post(
            f'/lists/{list_ob.id}/', 
            data={'item_text':''}
        )

        self.assertEqual(_response.status_code, 200)
        self.assertTemplateUsed(_response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(_response, expected_error)

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):

        self.client.post(
            '/lists/new',
            data={'item_text':'A new item to add'}
        )

        self.assertEqual(1, Item.objects.count())
        new_item = Item.objects.first()
        self.assertEqual('A new item to add', new_item.text)

    def test_redirects_after_POST(self):

        _response = self.client.post(
            '/lists/new', 
            data={'item_text':'A new item to add'}
        )

        new_list = List.objects.first()
        self.assertRedirects(_response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_the_home_page(self):

        _response = self.client.post('/lists/new', data={'item_text':''})
        self.assertEqual(_response.status_code, 200)
        self.assertTemplateUsed(_response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(_response, expected_error)
    
    def test_invalid_list_items_are_not_saved(self):

        self.client.post('/lists/new', data={'item_text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)