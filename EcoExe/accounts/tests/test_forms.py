#Authored by Sam Arrowsmith
from django.test import TestCase
from accounts.forms import SignUpForm

class SignUpFormTestCase(TestCase):

    valid_password = 'test123chairlaptoppassword'
    invalid_password = 'password1'

    def test_valid_form_signup(self):
        # Test valid form data
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': self.valid_password,  #password needs to match the confirmation password while also being complex enough to pass Django's authentication
            'password2': self.valid_password,
            'terms': True,
            'privacy': True
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_signup(self):
        # Test invalid form data with terms invalid
        form_data = {
            'username': '',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid_email',
            'password1': '',
            'password2': self.invalid_password + "1",    #not only are the passwords both too simple to use but they aren't matching --> diversified form validation
            'terms': False,
            'privacy': False   
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])  #assert username error
        self.assertEqual(form.errors['email'], ['Enter a valid email address.']) #assert email error
        self.assertEqual(form.errors['terms'], ['This field is required.'])  #assert terms error - checkbox should be ticked
        self.assertEqual(form.errors['privacy'], ['This field is required.'])  #assert privacy error - checkbox should be ticked

        #to account for the different password errors, we will redo the form; for the first run, we will check that common passwords and empty passwords are invalid
        self.assertEqual(form.errors['password1'], ['This field is required.'])  #assert empty password error
        self.assertEqual(form.errors['password2'], ['This password is too common.'])  #assert common password error

        #rebuild form with the issue being the passwords not matching
        form_data['password1'] = form_data['password2'] + "111" #string is distinct from password2
        form = SignUpForm(data=form_data)   # rebuild form
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.']) #assert passwords not matching error
        


    def test_form_save(self):
        # Test form save method - needs to be for valid data
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': self.valid_password,  #password needs to match the confirmation password while also being complex enough to pass Django's authentication
            'password2': self.valid_password,
            'terms': True,
            'privacy': True
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user_instance = form.save(commit=False)
        # Add assertions to check the user instance