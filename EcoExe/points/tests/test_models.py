#Authored by George Piper

from django.test import TestCase
from django.utils import timezone
from points.models import Points,DailyPoints
from accounts.models import User
from quiz.models import Quizzes
from gamekeeper.models import DailyQuizzes


class PointsModelTest(TestCase):
    '''
    The tests in this class check that the fields for the points model have the correct data in them when a row with a user and quiz is inserted into the table
    - setUpTestData establishes the row in the testing database
    - the tests themselves check that constraints are met (i.e. unique user/quiz ids) and that the data in the row is as expected based on the data entered in the set up
    '''
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='test_user', password='test_password')
        quiz = Quizzes.objects.create(points=100, time=120)
        Points.objects.create(user_id=user, quiz_id=quiz, points=50, timestamp=timezone.now())

    def test_user_id_foreign_key(self):
        point = Points.objects.get(id=1)
        self.assertEqual(point.user_id.username, 'test_user')

    def test_quiz_id_foreign_key(self):
        point = Points.objects.get(id=1)
        self.assertEqual(point.quiz_id.points, 100)

    def test_points_default_value(self):
        point = Points.objects.get(id=1)
        self.assertEqual(point.points, 50)

    def test_timestamp_default_value(self):
        point = Points.objects.get(id=1)
        self.assertIsNotNone(point.timestamp)

    def test_unique_constraint(self):
        # Attempt to create another Points object with the same user_id and quiz_id
        user = User.objects.get(username='test_user')
        quiz = Quizzes.objects.get(points=100)
        with self.assertRaises(Exception):
            Points.objects.create(user_id=user, quiz_id=quiz, points=50, timestamp=timezone.now())

class DailyPointsModelTest(TestCase):
    '''
    The tests here check that the daily points model in the database functions as expected
    - setUpTestData establishes a row with a user, quiz and date of that respective daily quiz
    - the tests then verify that the data was inserted correctly and that the database can be successfully queried
    - default values are also checked
    - uniqueness of the user and quiz ids are also tested
    '''

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='test_user', password='test_password')
        quiz = Quizzes.objects.create(points=100, time=120)
        date = DailyQuizzes.objects.create(date=timezone.now())
        DailyPoints.objects.create(user_id=user, quiz_id=quiz, date=date, points=50, timestamp=timezone.now())

    def test_user_id_foreign_key(self):
        daily_point = DailyPoints.objects.get(id=1)
        self.assertEqual(daily_point.user_id.username, 'test_user')

    def test_quiz_id_foreign_key(self):
        daily_point = DailyPoints.objects.get(id=1)
        self.assertEqual(daily_point.quiz_id.points, 100)

    def test_date_foreign_key(self):
        daily_point = DailyPoints.objects.get(id=1)
        self.assertIsNotNone(daily_point.date)

    def test_points_default_value(self):
        daily_point = DailyPoints.objects.get(id=1)
        self.assertEqual(daily_point.points, 50)

    def test_timestamp_default_value(self):
        daily_point = DailyPoints.objects.get(id=1)
        self.assertIsNotNone(daily_point.timestamp)

    def test_unique_constraint(self):
        # Attempt to create another DailyPoints object with the same user_id, quiz_id, and date
        user = User.objects.get(username='test_user')
        quiz = Quizzes.objects.get(points=100)
        date = DailyQuizzes.objects.get(date=timezone.now())
        with self.assertRaises(Exception):
            DailyPoints.objects.create(user_id=user, quiz_id=quiz, date=date, points=50, timestamp=timezone.now())


