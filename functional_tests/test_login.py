from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'bob@example.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Bob goes to the website and finds there's a new feature to log in.
        # He is prompted to enter the email and so does he do.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears that a email has been sent to him with the log in
        # URL
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her mail and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a a URL link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)

        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # He clicks it
        self.browser.get(url)

        # He is logged in!
        self.wait_to_be_logged_in(TEST_EMAIL) 

        # He now logs out of it
        self.browser.find_element_by_link_text('Log out').click()

        # He is logged out
        self.wait_to_be_logged_out(TEST_EMAIL)