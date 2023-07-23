from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Question

def create_question(question_text, days, hours=0, minutes=0, seconds=0):
    """Create questions"""

    time = timezone.now() + timedelta(days=days, hours=hours,
        minutes=minutes, seconds=seconds)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    return question

class QuestionModelTests(TestCase):
    def test_Was_published_recently_with_fture_question(self):
        """
        Was_published_recently returns False for questions whose\
        pub_date is in the future
        """
        
        future_question = create_question("future_question", 30)
        msg = "questions create in future time was NOT recently published."
        self.assertIs(future_question.was_published_recently(), False, msg)
        
    def test_was_published_recently_for_old_question(self):
        """
        Was_published_recently returns False for questions whose\
        pub_date is in the past
        """
        
        old_question = create_question("old_question", -30)
        msg = "questions create in past was NOT recently published."
        self.assertIs(old_question.was_published_recently(), False, msg)
        
    def test_was_published_recently_for_recent_question(self):
        """
        Was_published_recently returns True for questions whose\
        pub_date is recently
        """
        
        question = create_question("question", 0, -22, -59, -59)
        msg = "questions created recently published recently."
        self.assertIs(question.was_published_recently(), True, msg)
        