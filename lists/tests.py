from django.test import TestCase

# Create your tests here.
class ThisWillFailTesting(TestCase):

    def test_bad_at_maths(self):

        self.assertEquals(1 + 1, 3)