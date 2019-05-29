from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ListItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_lists(self):

        # Bob goes to the home page and accidentaly bumps the submit button
        # on an empty list item.

        # The home page refreshes, there is a error message saying that the 
        # list item cannot be empty.

        # He again tries to add a new valid item to the list, which works.

        # Perversely, he again tries to submit an empty list item, and again
        # comes across same error message on the lists page.

        self.fail('Finish the test')