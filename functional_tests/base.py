from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 10

def wait(fn):

    """
    Decorator to avoid explicit wait methods for the helper functions
    """
    def modified_fn(*args, **kwargs):

        start_time = time.time()

        while True:
            
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:

                if time.time() - start_time > MAX_WAIT:
                    raise e
                
                time.sleep(0.5)
    
    return modified_fn

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        # One day Bob wanted to go the To-Do website so he opened the browser
        # to visit the site
        self.browser = webdriver.Firefox()
        
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server

    def tearDown(self):
        # Gracefully, quits the browser 
        self.browser.quit()

    def get_item_input_box(self):

        return self.browser.find_element_by_id('id_text')

    def wait_for(self, fn):
        
        start_time = time.time()

        while True:
            
            try:
                return fn()
            
            except (AssertionError, WebDriverException) as e:
            
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    @wait
    def wait_for_a_item_present_in_the_list(self, row_text):

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email):
        
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)
    
    @wait
    def wait_to_be_logged_out(self, email):

        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)