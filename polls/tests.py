from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):
    def test_Was_published_recently_with_fture_question(self):
        """
        was_published_recently returns False for questions whose\
        pub_date is in the future
        """
        
        future_time = timezone.now()+timedelta(days=33) 
        future_question = Question.objects.create(
            question_text="future_question", pub_date=future_time)
        msg = "questions create in future time was NOT recently published."
        self.assertIs(future_question.was_published_recently(), False, msg)
        
    def test_was_published_recently_for_old_question(self):
        """
        was_published_recently returns False for questions whose\
        pub_date is in the past
        """
        
        old_time = timezone.now() - timedelta(days=1, seconds=1)
        old_question = Question.objects.create(
            question_text="old_question", pub_date=old_time)
        msg = "questions create in past was NOT recently published."
        self.assertIs(old_question.was_published_recently(), False, msg)
        
    def test_was_published_recently_for_recent_question(self):
        """
        was_published_recently returns True for questions whose\
        pub_date is recently
        """
        
        time = timezone.now() - timedelta(hours=23,minutes=59, seconds=59)
        question = Question.objects.create(
            question_text="question", pub_date=time)
        msg = "questions create recently published recently."
        self.assertIs(question.was_published_recently(), True, msg)
        