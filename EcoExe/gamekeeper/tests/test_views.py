#Authored by Sam Arrowsmith
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from accounts.models import User
from gamekeeper.forms import LoginForm


class LoginViewTest(TestCase):
    #this class tests the login view and that it returns the correct status codes from http responses, ensuring valid users can log in and invalid users get the respective error message
    def setUp(self):
        self.client = Client()
        self.valid_user = User.objects.create_user(username='validgamekeeper', password='testpasswordforgamekeeper987123', is_gamekeeper=True)
        self.login_url = reverse('login')
    
    def test_login_with_valid_credentials(self):
        #verifies that the correct response code (200 for success) is returned when valid gamekeeper credentials are input
        response = self.client.post(self.login_url, {'username': 'validgamekeeper', 'password': 'testpasswordforgamekeeper987123'}) # Simulate a form submission
        self.assertEquals(response.status_code, 200)    #asserts that the correct code is found

     
    def test_login_with_invalid_credentials(self):
        #verifies that the correct error message is shown when wrong credentials are used
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'}) # Simulate a form submission with invalid credentials
        self.assertContains(response, "Invalid Credentials") # Assert that the login form is redisplayed with an error message