from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

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
    
    def test_cannot_save_empty_list_items(self):

        list_ob = List.objects.create()
        item = Item(list=list_ob, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()


