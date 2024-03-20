#Authored by Sam Arrowsmith and George Piper
from django.test import TestCase

from django.test import SimpleTestCase
from gamekeeper.forms import LoginForm,QuizCreationForm,QRCreationForm,TreasureHuntCreationForm,SetDailyForm

class TestLoginForm(SimpleTestCase):
    # tests that when valid data is input into the login form that it is considered valid
    def test_valid_form(self):
        form = LoginForm(data={
            'username': 'test_user',
            'password': 'password123'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_username(self):
        # tests that the form is recognized as invalid when username is missing from login
        form = LoginForm(data={
            'password': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_invalid_form_missing_password(self):
        # tests that the form is recognized as invalid when password is missing from login
        form = LoginForm(data={
            'username': 'test_user',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['This field is required.'])

    def test_invalid_form_empty_data(self):
        # tests that the form is recognized as invalid when both username and password are missing from login
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])
        self.assertEqual(form.errors['password'], ['This field is required.'])

class TestQuizCreationForm(SimpleTestCase):
    # tests that a quiz creation form is considered valid when valid data is input - the data won't break any rules and constraints of the models used later on 
    def test_valid_form(self):
        form = QuizCreationForm(data={
            'quiz_name': 'Test Quiz',
            'points_per_question': 10,
            'extra_field_count': 2,
            'time': 60,
            'extra_field_1': 'Question 1',
            'extra_field_2': 'Answer 1',
            'extra_field_3': 'Question 2',
            'extra_field_4': 'Answer 2',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_data(self):
        # verifies that the form is deemed invalid when fields are left blank
        form = QuizCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['quiz_name'], ['This field is required.'])
        self.assertEqual(form.errors['points_per_question'], ['This field is required.'])
        self.assertEqual(form.errors['extra_field_count'], ['This field is required.'])
        self.assertEqual(form.errors['time'], ['This field is required.'])

class TestQRCreationForm(SimpleTestCase):
    # tests that a QR creation form is considered valid when valid data is input - the data won't break any rules and constraints of the models used later on 
    def test_valid_form(self):
        form = QRCreationForm(data={
            'qr_name': 'Test QR',
            'latitude': 12.345,
            'longitude': 67.890,
            'location_name': 'Test Location',
            'points': 10,
            'extra': 'Some extra data'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_data(self):
        # verifies that the form is deemed invalid when fields are left blank
        form = QRCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['qr_name'], ['This field is required.'])
        self.assertEqual(form.errors['latitude'], ['This field is required.'])
        self.assertEqual(form.errors['longitude'], ['This field is required.'])
        self.assertEqual(form.errors['location_name'], ['This field is required.'])
        self.assertEqual(form.errors['points'], ['This field is required.'])

    def test_valid_form_optional_extra_data(self):
        # verifies that the form is deemed valid when the extra info field is left blank - it isn't compulsory so the form shouldn't be deemed invalid for missing it
        form = QRCreationForm(data={
            'qr_name': 'Test QR',
            'latitude': 12.345,
            'longitude': 67.890,
            'location_name': 'Test Location',
            'points': 10,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_invalid_latitude(self):
        # self-explanatory
        form = QRCreationForm(data={
            'qr_name': 'Test QR',
            'latitude': 'invalid',  # Latitude should be a float
            'longitude': 67.890,
            'location_name': 'Test Location',
            'points': 10,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['latitude'], ['Enter a number.'])

    def test_invalid_form_invalid_longitude(self):
        # self explanatory
        form = QRCreationForm(data={
            'qr_name': 'Test QR',
            'latitude': 12.345,
            'longitude': 'invalid',  # Longitude should be a float
            'location_name': 'Test Location',
            'points': 10,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['longitude'], ['Enter a number.'])

class TestTreasureHuntCreationForm(SimpleTestCase):
    # tests that the form for treasure hunt creation is valid when data which doesn't break the constraints of the models is input
    def test_valid_form(self):
        form = TreasureHuntCreationForm(data={
            'treasure_hunt_name': 'Test Treasure Hunt',
            'bonus_points': 50,
            'extra_field_count': 2,
            'extra_field_1': 'Clue 1',
            'extra_field_2': 'Clue 2',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_data(self):
        # if data is missing, the form needs to be recognized as invalid
        form = TreasureHuntCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['treasure_hunt_name'], ['This field is required.'])
        self.assertEqual(form.errors['bonus_points'], ['This field is required.'])
        self.assertEqual(form.errors['extra_field_count'], ['This field is required.'])

class TestSetDailyForm(SimpleTestCase):
    def test_valid_form(self):
        # checks that the form is deemed valid when relevant data is input
        form_data = {
            'quiz': 'Test Quiz',
            'date': '2024-03-20',  # Assuming today's date
        }
        form = SetDailyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_data(self):
        # if data is missing, form needs to be recognized as invalid
        form_data = {}
        form = SetDailyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('quiz', form.errors)
        self.assertIn('date', form.errors)

