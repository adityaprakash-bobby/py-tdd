from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        # One day Bob wanted to go the To-Do website so he opened the browser to visit the site
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # Gracefully, quits the browser 
        self.browser.quit()

    def test_that_he_can_start_a_list_and_retrieve_it_later(self):
        # He opened the browser to visit the To-Do application on the site by
        # typing the address
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == '1: Buy Turbos' for row in rows),
        #     f"New To-Do element did not appear in the table. Contents were:\n{table.text}"
        # )
        self.assertIn(
            '1: Buy Turbos',
            [row.text for row in rows]
        )
        
        # There is still a text box inviting him to add another item. He
        # enters "Use turbos in my Nissan 240sx"
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use turbos in my Nissan 240sx')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on his list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            '1: Buy Turbos',
            [row.text for row in rows]
        )
        self.assertIn(
            '2: Use turbos in my Nissan 240sx',
            [row.text for row in rows]
        )

        self.fail('Finish the tests!')
        # Bob wonders whether the site will remember his list. Then he sees
        # that the site has generated a unique URL for him -- there is some
        # explanatory text to that effect.

        # He visits that URL - his to-do list is still there.

        # Satisfied, he goes back to sleep

if __name__ == "__main__":
    unittest.main(warnings='ignore')
