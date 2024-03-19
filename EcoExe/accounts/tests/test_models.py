#Authored by Sam Arrowsmith
from django.test import TestCase
from accounts.models import User

class UserModelTestCase(TestCase):
    def setUp(self):
        # Set up test data
        User.objects.create_user(username="testuser", password="test123", email="test@example.com")

    def test_user_creation(self):
        # Test user creation and default values
        test_user = User.objects.get(username="testuser")
        self.assertFalse(test_user.is_gamekeeper)  # Check that the user isn't a gamekeeper, as in the setup, we have defined it to not be
        self.assertEqual(test_user.avatar.url, '/media/default.jpg')  # Check default value for avatar
        self.assertEqual(test_user.bio, None)  # Check default value for bio stored in the database - none
