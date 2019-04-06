from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        # One day Bob wanted to go the To-Do website so he opened the browser to visit the site
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # Gracefully, quits the browser 
        self.browser.quit()

    def test_that_he_can_start_a_list_and_retrieve_it_later(self):
        # He opened the browser to visit the To-Do application on the site by typing the address
        self.browser.get('http://localhost:8000')

        # The title appears as 'To-Do' on the browser window title bar
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # He is invited to enter a to-do item straight away

        # He types "Buy turbos" into a text box

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy turbos" as an item in a to-do list

        # There is still a text box inviting her to add another item. He
        # enters "Use turbos in my Nissan 240sx"

        # The page updates again, and now shows both items on his list

        # Bob wonders whether the site will remember her list. Then he sees
        # that the site has generated a unique URL for him -- there is some
        # explanatory text to that effect.

        # He visits that URL - his to-do list is still there.

        # Satisfied, he goes back to sleep

if __name__ == "__main__":
    unittest.main(warnings='ignore')