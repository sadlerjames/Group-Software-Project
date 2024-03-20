from django.test import TestCase
from django.utils import timezone
from points.models import Points,DailyPoints
from accounts.models import User
from quiz.models import Quizzes

class PointsModelTest(TestCase):
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
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='test_user', password='test_password')
        quiz = Quizzes.objects.create(points=100, time=120)
        DailyPoints.objects.create(user_id=user, quiz_id=quiz, points=50, timestamp=timezone.now())

    def test_user_id_foreign_key(self):
        daily_point = DailyPoints.objects.get(id=1)
        self.assertEqual(daily_point.user_id.username, 'test_user')

    def test_quiz_id_foreign_key(self):
        daily_point = DailyPoints.objects.get(id=1)
        self.assertEqual(daily_point.quiz_id.points, 100)

    def test_points_default_value(self):
        daily_point = DailyPoints.objects.get(id=1)
        self.assertEqual(daily_point.points, 50)

    def test_timestamp_default_value(self):
        daily_point = DailyPoints.objects.get(id=1)
        self.assertIsNotNone(daily_point.timestamp)

    def test_unique_constraint(self):
        # Attempt to create another DailyPoints object with the same user_id and quiz_id
        user = User.objects.get(username='test_user')
        quiz = Quizzes.objects.get(points=100)
        with self.assertRaises(Exception):
            DailyPoints.objects.create(user_id=user, quiz_id=quiz, points=50, timestamp=timezone.now())

