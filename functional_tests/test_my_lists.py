from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server

User = get_user_model()

class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a session cookie, we first need to visit the domain. For this
        ## the 404 page loads the quickest
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))
    
    def test_logged_in_users_lists_are_saved_as_my_lists(self):

        email = 'bob@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Bob is logged-in
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
    
    def test_logged_in_users_list_is_saved_as_my_lists(self):

        # Bob goes to the site and logs-in
        self.create_pre_authenticated_session('bob@example.com')

        # Bob goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.add_list_item('Lambo Chassis')
        self.add_list_item('Extra frames to build the damaged frame')
        first_list_url = self.browser.current_url

        # She notices "My lists" for the first time
        self.browser.find_element_by_link_text('My lists').click()

        # She sees there that the list is already in there and named according
        # the first list item.
        self.wait_for(
            lambda:self.browser.find_element_by_link_text('Lambo Chassis')
        )

        self.browser.find_element_by_link_text('Lambo Chassis').click()
        self.wait_for(
            lambda:self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Just to see that another list link is created, he starts another list
        self.browser.get(self.live_server_url)
        self.add_list_item('Get RTX2080i')
        self.add_list_item('God! It is pricy')
        second_list_url = self.browser.current_url

        # Under 'My lists', his new list appears
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Get RTX2080i')
        )

        self.browser.find_element_by_link_text('Get RTX2080i').click()
        self.wait_for(
            lambda:self.assertEqual(self.browser.current_url, second_list_url)
        )

        # He then logs out of the site, to find "My lists" disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_link_text('My lists'),
            []
        ))