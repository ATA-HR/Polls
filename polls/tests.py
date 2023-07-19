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
        msg = "questions create in future time are NOT recently published."
        self.assertIs(future_question.was_published_recently(), False, msg)