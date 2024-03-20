#Authored by George Piper
from django.test import TestCase
from gamekeeper.models import DailyQuizzes
from quiz.models import Quizzes  # Assuming this is your quiz model
from datetime import date


class DailyQuizzesTest(TestCase):
    def setUp(self):
        # Create a sample quiz
        self.quiz = Quizzes.objects.create(id=1, points=100, time=60)

    def test_daily_quiz_creation(self):
        # Create a daily quiz
        daily_quiz = DailyQuizzes.objects.create(
            date=date.today(),  # Assuming today's date
            quiz_id=self.quiz,
            time_limit=30
        )

        # Retrieve the daily quiz from the database
        saved_daily_quiz = DailyQuizzes.objects.get(date=date.today())

        # Check if the retrieved daily quiz matches the one created
        self.assertEqual(saved_daily_quiz.date, daily_quiz.date)
        self.assertEqual(saved_daily_quiz.quiz_id, self.quiz)
        self.assertEqual(saved_daily_quiz.time_limit, 30)

    def test_daily_quiz_deletion(self):
        # Create a daily quiz
        daily_quiz = DailyQuizzes.objects.create(
            date=date.today(),  # Assuming today's date
            quiz_id=self.quiz,
            time_limit=30
        )

        # Delete the daily quiz
        daily_quiz.delete()

        # Check if the daily quiz is deleted
        with self.assertRaises(DailyQuizzes.DoesNotExist):
            DailyQuizzes.objects.get(date=date.today())

    def test_daily_quiz_update(self):
        # Create a daily quiz
        daily_quiz = DailyQuizzes.objects.create(
            date=date.today(),  # Assuming today's date
            quiz_id=self.quiz,
            time_limit=30
        )

        # Update the time limit of the daily quiz
        daily_quiz.time_limit = 45
        daily_quiz.save()

        # Retrieve the updated daily quiz from the database
        updated_daily_quiz = DailyQuizzes.objects.get(date=date.today())

        # Check if the time limit is updated
        self.assertEqual(updated_daily_quiz.time_limit,45)
