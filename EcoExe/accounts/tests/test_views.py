#Authored by Sam Arrowsmith
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User

class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client() #creates a client which can send GET and POST requests for testing purposes
        self.signup_url = reverse('signup')  

    def test_signup_view_get(self):
        #checks that the view used for a GET request is the signup page
        response = self.client.get(self.signup_url)     
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')


    '''
    This function is still faulty, there are several redirects and need to figure out which one is desired
    '''
    def test_signup_view_post_valid_form(self):
        # Create a valid form data for signing up a new user
        valid_form_data = {
            'username' : 'testuser',
            'email' : 'email@email.com',
            'first_name' : 'test',
            'last_name' : 'user',
            'password1': 'testpassword123wordpasstest',
            'password2': 'testpassword123wordpasstest',
            'terms' : True,
            'privacy' : True
        }

        response = self.client.post(self.signup_url, valid_form_data)


        #self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful signup

        self.assertRedirects(response, '/accounts/login')  

        # Check if the user is created
        user_created = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_created)

    def test_signup_view_post_invalid_form(self):
        # Create an invalid form data for signing up a new user
        invalid_form_data = {
            #a blank form will not be valid, hence this is suitable
        }

        response = self.client.post(self.signup_url, invalid_form_data)
        self.assertEqual(response.status_code, 200)  # Expecting to stay on the signup page
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertContains(response, 'This field is required')  # Add an appropriate error message to check for

        # Check if the user is not created
        user_created = User.objects.filter(username='testuser').exists()
        self.assertFalse(user_created)