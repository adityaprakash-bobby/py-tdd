from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # User goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He/she notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        ) 

        # He/she starts a new list and finds that the input is nicely centered
        # too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_a_item_present_in_the_list('1: testing')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )