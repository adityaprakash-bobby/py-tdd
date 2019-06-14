from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from lists.models import Item, List

User = get_user_model()

class TestItemModels(TestCase):
    
    def test_default_text(self):

        item = Item()
        self.assertEqual(item.text, '')
    
    def test_item_is_related_to_list(self):

        list_ob = List.objects.create()
        item = Item()
        item.list = list_ob
        item.save()
        self.assertIn(item, list_ob.item_set.all())
    
    def test_ordering_of_items(self):

        list_ob = List.objects.create()
        item1 = Item.objects.create(text='i1', list=list_ob)
        item2 = Item.objects.create(text='i2', list=list_ob)
        item3 = Item.objects.create(text='i3', list=list_ob)

        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representaion(self):
        
        list_ob = List.objects.create()
        item = Item(text='some text', list=list_ob)

        self.assertEqual(
            str(item),
            'some text'
        )

    def test_cannot_save_empty_list_items(self):

        list_ob = List.objects.create()
        item = Item(list=list_ob, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):

        list_ob = List.objects.create()
        Item.objects.create(text='random', list=list_ob)

        with self.assertRaises(ValidationError):
            
            item = Item(text='random', list=list_ob)
            item.full_clean()

    def test_can_save_same_items_to_different_lists(self):

        list1 = List.objects.create()
        list2 = List.objects.create()

        Item.objects.create(list=list1, text='random')
        item = Item(list=list2, text='random')

        item.full_clean()

class TestListModel(TestCase):

    def test_get_absolute_URL(self):

        list_ob = List.objects.create()
        self.assertEqual(list_ob.get_absolute_url(), f'/lists/{list_ob.id}/')
    
    def test_lists_can_have_owner(self):

        user = User.objects.create(email='a@b.com')
        list_ob = List.objects.create(owner=user)
        self.assertIn(list_ob, user.list_set.all())

    def test_list_owner_is_optional(self):
        List.objects.create()

    def test_list_name_is_first_item_text(self):

        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')