import re
import os
import time
import poplib
from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def wait_for_mail(self, test_email, subject):

        if not self.staging_server:

            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')

        try:
            inbox.user(test_email)
            inbox.pass_(os.environ.get('YAHOO_PASSWORD'))

            while (time.time() - start) < 60:
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting message', i)
                    _, lines, _ =  inbox.retr(i)
                    lines = [l.decode('utf-8') for l in lines]
                 
                    if f'Subject: {subject}' in lines:
                        email_id = 1
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        # Bob goes to the website and finds there's a new feature to log in.
        # He is prompted to enter the email and so does he do.
        if self.staging_server:
            test_email = 'testinggoatisthebest@yahoo.com'
        else:
            test_email = 'bob@example.com'
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears that a email has been sent to him with the log in
        # URL
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her mail and finds a message
        body = self.wait_for_mail(test_email, SUBJECT)

        # It has a a URL link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)

        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # He clicks it
        self.browser.get(url)

        # He is logged in!
        self.wait_to_be_logged_in(test_email) 

        # He now logs out of it
        self.browser.find_element_by_link_text('Log out').click()

        # He is logged out
        self.wait_to_be_logged_out(test_email)