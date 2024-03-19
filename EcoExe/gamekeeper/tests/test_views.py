#Authored by Sam Arrowsmith
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import login, logout
from accounts.models import User
from gamekeeper.forms import LoginForm

'''unfinished, tests here don't work'''
class LoginViewTest(TestCase):
    def test_login_with_valid_credentials(self):
        # Create a user for testing
        User.objects.create_user(username='validgamekeeper', password='testpasswordforgamekeeper987123', is_gamekeeper=True)
        
        client = Client()
        response = client.post('/login/', {'username': 'validgamekeeper', 'password': 'testpasswordforgamekeeper987123'}) # Simulate a form submission
        print("TEST VALID : ", response)
        # Assert that the user is redirected to the dashboard
        self.assertRedirects(response, '/gamekeeper/dashboard/')
        
    def test_login_with_invalid_credentials(self):
        client = Client()
        response = client.post('/login/', {'username': 'invaliduser', 'password': 'invalidpassword'}) # Simulate a form submission with invalid credentials
        print("TEST INVALID : ", response)
        # Assert that the login form is redisplayed with an error message
        self.assertContains(response, "Invalid Credentials")