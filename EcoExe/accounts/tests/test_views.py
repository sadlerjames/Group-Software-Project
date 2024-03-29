#Authored by Sam Arrowsmith
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from django.contrib.auth import login, logout

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_redirect_authenticated_user_to_dashboard(self):
        #verifies that if the link to login is input while an authenticated user is already signed in, that the page redirects to the dashboard
        self.client.login(username='testuser', password='12345')

        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)  # Verify the response code for login

        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)  # Verify the response code for dashboard

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': '12345'})
        self.assertRedirects(response, self.dashboard_url)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertContains(response, "Invalid Credentials", status_code=200)

class DeleteAccountViewTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.client = Client()
        self.user = User.objects.create_user(username='tobedeleted', password='12345mrdeletey54321')

    def test_delete_account_post(self):
        #tests that after logging in with an account, it gets deleted and removed from the database following a POST request
        self.client.login(username='tobedeleted', password='12345mrdeletey54321')  # Log in as the user created in setup
        response = self.client.post(reverse('delete_account'))  # Make a POST request to delete the account
        self.assertFalse(User.objects.filter(username='tobedeleted').exists()) # Check if the user account is deleted
        self.assertFalse('_auth_user_id' in self.client.session) # Check if the user is logged out
        self.assertEqual(response.status_code, 302) # assert that the page will redirect


class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client() #creates a client which can send GET and POST requests for testing purposes
        self.signup_url = reverse('signup')  
        self.authenticated_user = User.objects.create_user(username='test_authenticated_user', password='12345pass')   
        #used for checking that if the signup page url is input while an authenticated user is signed in, they just get redirected to the dashboard - standard way to sign up is to log out completely

    def test_signup_view_get(self):
        #checks that the view used for a GET request is the signup page
        response = self.client.get(self.signup_url)     
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')


    def test_redirect_authenticated_user_to_dashboard(self):
        #verifies that if the link to signup is input while an authenticated user is already signed in, that the page redirects to the dashboard
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)  # Verify the response code after logging in and going to signup - 200 as it issuccessful

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Verify the response code for dashboard - 302 for redirecting to the dashboard 
        
    
    def test_signup_view_post_valid_form_new_user(self):
        # Create a valid form data for signing up a new user - follow the code path where it redirects them to log in after successful creation
        name = 'viyebqnc'
        valid_form_data = {
            'username' : name,
            'email' : 'eml@email.com',
            'first_name' : 'test',
            'last_name' : 'user',
            'password1': 'testpassword123wordpasstest',
            'password2': 'testpassword123wordpasstest',
            'terms' : True,
            'privacy' : True
        }

        response = self.client.post(self.signup_url, valid_form_data)   #posts the valid form data
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful signup, verify the relevant response code

        response = self.client.get(reverse('login'), follow=True)
        self.assertEqual(response.status_code, 200)  # content has been successfully requested, verify the response code

        # Check if the user is created
        user_created = User.objects.filter(username=name).exists()
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