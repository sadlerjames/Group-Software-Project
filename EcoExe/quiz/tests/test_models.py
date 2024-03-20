from django.test import TestCase
from quiz.models import Quizzes

class QuizzesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Quizzes.objects.create(points=100, time=120)

    def test_points_default_value(self):
        quiz = Quizzes.objects.get(id=1)
        self.assertEqual(quiz.points, 100)

    def test_time_default_value(self):
        quiz = Quizzes.objects.get(id=1)
        self.assertEqual(quiz.time, 120)

    def test_str_method(self):
        quiz = Quizzes.objects.get(id=1)
        self.assertEqual(str(quiz), '1')

    def test_id_auto_generated(self):
        quiz = Quizzes.objects.get(id=1)
        self.assertIsNotNone(quiz.id)
