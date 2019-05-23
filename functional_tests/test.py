from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        # One day Bob wanted to go the To-Do website so he opened the browser
        # to visit the site
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # Gracefully, quits the browser 
        self.browser.quit()

    def wait_for_a_item_present_in_the_list(self, row_text):

        start_time = time.time()

        while True:
            
            try:
            
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                
                return

            except (AssertionError, WebDriverException) as e:

                if time.time() - start_time > MAX_WAIT:
                    raise e
                
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # He opened the browser to visit the To-Do application on the site by
        # typing the address
        self.browser.get(self.live_server_url)

        # The title appears as 'To-Do' on the browser window title bar and 
        # headinf of to-do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a To-Do item'
        )

        # He types "Buy turbos" into a text box
        input_box.send_keys('Buy Turbos')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy turbos" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)
        self.wait_for_a_item_present_in_the_list('1: Buy Turbos')
        
        # There is still a text box inviting him to add another item. He
        # enters "Use turbos in my Nissan 240sx"
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use turbos in my Nissan 240sx')
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.wait_for_a_item_present_in_the_list('1: Buy Turbos')
        self.wait_for_a_item_present_in_the_list('2: Use turbos in my Nissan 240sx')

        # self.fail('Finish the tests!')
        # Bob wonders whether the site will remember his list. Then he sees
        # that the site has generated a unique URL for him -- there is some
        # explanatory text to that effect.

        # He visits that URL - his to-do list is still there.

        # Satisfied, he goes back to sleep

    def test_multiple_users_can_start_a_list_at_different_URLS(self):
        
        # Bob starts a new list
        self.browser.get(self.live_server_url)
        
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy Turbos')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_a_item_present_in_the_list('1: Buy Turbos')

        # He notices that he has a unique URL for his list
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, '/lists/.+') 

        # A new user Alice wants to visit the site (So we close the browser to
        # ensure that no cached data of Bob is shown)
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Alice visits the website and finds no data of Bob on the screen
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Turbos', page_text)
        self.assertNotIn('Use turbos in my new Nissan 240sx', page_text)

        # Alice starts a new list of her own, so she types down them
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy Milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_a_item_present_in_the_list('1: Buy Milk')

        # Alice observes that she gets her unique URL for her list
        alice_list_url = self.browser.current_url
        self.assertRegex(alice_list_url, '/lists/.+')
        self.assertNotEqual(bob_list_url, alice_list_url)

        # There is no sign of Bob's list again
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Turbos', page_text)
        self.assertIn('Buy Milk', page_text)

        # Satisfied they both go to sleep
        self.fail('Finish the tests!')

    