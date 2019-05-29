from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ListItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_lists(self):

        # Bob goes to the home page and accidentaly bumps the submit button
        # on an empty list item.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, there is a error message saying that the 
        # list item cannot be empty.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # He again tries to add a new valid item to the list, which works.
        self.browser.find_element_by_id('id_new_item').send_keys("Buy Turbos")
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_a_item_present_in_the_list('1: Buy Turbos')
        
        # Perversely, he again tries to submit an empty list item, and again
        # comes across same error message on the lists page.
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # She then correctly inserts the data
        self.browser.find_element_by_id('id_new_item').send_keys("Buy House")
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_a_item_present_in_the_list("1: Buy Turbos")
        self.wait_for_a_item_present_in_the_list("1: Buy House")
