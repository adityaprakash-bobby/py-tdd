from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from lists.models import Item, List
from lists.views import home_page
from lists.forms import (
    ItemForm, EMPTY_ITEM_ERROR,
    ExistingListItemForm, DUPLICATE_ITEM_ERROR
)
from unittest import skip

class TestForHomePage(TestCase):

    def test_root_url_resolves_the_home_page_view(self):

        self.assertEqual(resolve('/').func, home_page)

    def test_home_page_returns_correct_html(self):

        _response = self.client.get('/')
        self.assertTemplateUsed(_response, 'home.html')

    def test_html_renders_the_correct_form(self):

        _response = self.client.get('/')
        self.assertIsInstance(_response.context['form'], ItemForm)

class ListViewTest(TestCase):

    def post_invalid_input(self):
        
        list_ob = List.objects.create()
        return self.client.post(
            f'/lists/{list_ob.id}/',
            data={'text': ''}
        )
       
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

    def test_shows_the_item_form(self):

        list_ob = List.objects.create()
        _response = self.client.get(f'/lists/{list_ob.id}/')
        self.assertIsInstance(_response.context['form'], ItemForm)
        self.assertContains(_response, 'name="text"')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/', 
            data={'text':'A new item to add to existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item to add to existing list')
        self.assertEqual(correct_list, new_item.list)

    def test_POST_redirects_to_list_view(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        _response = self.client.post(f'/lists/{correct_list.id}/', 
            data={'text':'A new item to add to existing list'}
        )

        self.assertRedirects(_response, f'/lists/{correct_list.id}/')

    def test_for_invalid_input_nothing_saved_to_db(self):

        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):

        _response = self.post_invalid_input()
        self.assertEqual(_response.status_code, 200)
        self.assertTemplateUsed(_response, 'list.html')
    
    def test_for_invalid_input_passes_form_to_template(self):

        _response = self.post_invalid_input()
        self.assertIsInstance(_response.context['form'], ItemForm)
    
    def test_for_invalid_input_shows_error_on_page(self):

        _response = self.post_invalid_input()
        self.assertContains(_response, escape(EMPTY_ITEM_ERROR))

    @skip
    def test_duplication_error_ends_up_in_the_list_page(self):

        list_ob = List.objects.create()
        Item.objects.create(text='text item', list=list_ob)
        
        _response = self.client.post(
            f'/lists/{list_ob.id}/',
            data={
                'text': 'text item'
        })

        expected_error = escape("You've already got this in your list")
        self.assertContains(_response, expected_error)
        self.assertTemplateUsed('list.html')
        self.assertEqual(Item.objects.count(), 1)

class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):

        list_ob = List.objects.create()
        form = ExistingListItemForm(for_list=list_ob)
        self.assertIn('placeholder="Enter a To-Do item"', form.as_p())

    def test_form_validaton_for_empty_item(self):

        list_ob = List.objects.create()
        form = ExistingListItemForm(for_list=list_ob, data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplcate_item(self):

        list_ob = List.objects.create()
        Item.objects.create(list=list_ob, text='Duplicate')
        form = ExistingListItemForm(for_list=list_ob, data={'text':'Duplicate'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):

        self.client.post(
            '/lists/new',
            data={'text':'A new item to add'}
        )

        self.assertEqual(1, Item.objects.count())
        new_item = Item.objects.first()
        self.assertEqual('A new item to add', new_item.text)

    def test_redirects_after_POST(self):

        _response = self.client.post(
            '/lists/new', 
            data={'text':'A new item to add'}
        )

        new_list = List.objects.first()
        self.assertRedirects(_response, f'/lists/{new_list.id}/')
    
    def test_invalid_list_items_are_not_saved(self):

        self.client.post('/lists/new', data={'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_homepage(self):

        _response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(_response.status_code, 200)
        self.assertTemplateUsed(_response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):

        _response = self.client.post('/lists/new', data={'text':''})
        expected_error = escape("You can't have an empty list item")
        self.assertContains(_response, expected_error)
    
    def test_invalid_input_passes_form_to_home_template(self):

        _response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(_response.context['form'], ItemForm)

