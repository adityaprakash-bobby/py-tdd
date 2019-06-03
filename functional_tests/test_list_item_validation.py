from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
import time

class ListItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
    
    def test_cannot_add_empty_lists(self):

        # Bob goes to the home page and accidentaly bumps the submit button
        # on an empty list item.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request but does not load the list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # He again starts typing in to the text field to see that the error
        # disappears
        self.get_item_input_box().send_keys('Buy Turbos')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))


        # He again tries to add a new valid item to the list, which works.
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_a_item_present_in_the_list('1: Buy Turbos')

        # Perversely, he again tries to submit an empty list item, and again
        # comes across same error message on the lists page.
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # She then correctly inserts the data
        self.get_item_input_box().send_keys("Buy House")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_a_item_present_in_the_list("2: Buy House")
        self.wait_for_a_item_present_in_the_list("1: Buy Turbos")
    
    def test_cannot_add_duplicate_items(self):

        # Bob visits the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy hummus')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_a_item_present_in_the_list('1: Buy hummus')

        # She accidentally tries to add another item which is already presesnt
        # in the list
        self.get_item_input_box().send_keys('Buy hummus')
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # He gets an helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))
    
    def test_error_messages_are_cleared_on_input(self):

        # Bob visits the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy hummus')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_a_item_present_in_the_list('1: Buy hummus')

        # She accidentally tries to add another item which is already presesnt
        # in the list
        self.get_item_input_box().send_keys('Buy hummus')
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # He gets an helpful error message
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # He starts typing in the input box again and sees the error message 
        # disappear
        self.get_item_input_box().send_keys('a')
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))