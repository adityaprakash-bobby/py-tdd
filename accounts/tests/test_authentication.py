from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()

class AuthenticateTest(TestCase):

    def test_returns_NONE_if_no_such_token(self):

        result = PasswordlessAuthenticationBackend().authenticate(
            'no-such-token'
        )

        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):

        email = 'bob@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)

        self.assertEqual(new_user, user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):

        email = 'bob@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)

        self.assertEqual(existing_user, user)

class GetUserTest(TestCase):

    def test_gets_user_by_email(self):

        User.objects.create(email='alice@example.com')
        desired_user = User.objects.create(email='bob@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'bob@example.com'
        )

        self.assertEqual(found_user, desired_user)
    
    def test_returns_NONE_if_no_user_with_that_email(self):

        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('bob@example.com')
        )