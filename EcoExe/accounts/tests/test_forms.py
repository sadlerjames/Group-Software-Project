#Authored by Sam Arrowsmith
from django.test import TestCase
from accounts.forms import SignUpForm

class SignUpFormTestCase(TestCase):
    def test_valid_form(self):
        # Test valid form data
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'test123chairlaptoppassword',  #password needs to match the confirmation password while also being complex enough to pass Django's authentication
            'password2': 'test123chairlaptoppassword',
            'terms': True,
            'privacy': True
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test invalid form data
        form_data = {
            'username': '',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid_email',
            'password1': 'test123',
            'password2': 'test123',
            'terms': False,
            'privacy': False    #due to the privacy policy etc, these need to be True so to invalidate the form data, set them to false.
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])
        # Add more assertions for other expected errors

    def test_form_save(self):
        # Test form save method - needs to be for valid data
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'test123chairlaptoppassword',  #password needs to match the confirmation password while also being complex enough to pass Django's authentication
            'password2': 'test123chairlaptoppassword',
            'terms': True,
            'privacy': True
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user_instance = form.save(commit=False)
        # Add assertions to check the user instance