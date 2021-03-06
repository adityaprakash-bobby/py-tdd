from django.test import TestCase
from lists.forms import (
    ItemForm, ExistingListItemForm, 
    EMPTY_ITEM_ERROR
)
from lists.models import Item, List

class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):

        form = ItemForm()
        self.assertIn('placeholder="Enter a To-Do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):

        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):

        list_ob = List.objects.create()
        form = ItemForm(data={'text': 'do-me'})
        new_item = form.save(for_list=list_ob)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do-me')
        self.assertEqual(new_item.list, list_ob)
    
class ExistingItemFormTest(TestCase):

    def test_form_save(self):

        list_ob = List.objects.create()
        form = ExistingListItemForm(for_list=list_ob, data={'text':'new item'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])