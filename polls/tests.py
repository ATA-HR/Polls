from datetime import timedelta
from django.db.models import query

from django.test import TestCase
from django.utils import timezone
# from django.test import Client
from django.urls import reverse

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
           
class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """if no question exist returns no poll available"""
        response = self.client.get(reverse("poll:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response.context["latest_questions_list"], [])
    
    def test_future_question(self):
        """question with pub_date in the future aren't displayed in index page"""
        question = create_question("future_question", 3)
        response = self.client.get(reverse("poll:index"))
        self.assertContains(response, "No polls available")
        
    def test_past_question(self):
        """question with pub_date in the future aren't displayed in index page"""
        question = create_question("past_question", -3)
        respnse = self.client.get(reverse("poll:index"))
        self.assertQuerysetEqual(respnse.context["latest_questions_list"], [question])
        
    def test_past_and_future_question(self):
        """for questions in past and in future, just questions with pub_date in \
            past are displayed"""
        future_question = create_question("past_question", 3)
        past_question = create_question("past_question", -3)
        respnse = self.client.get(reverse("poll:index"))
        self.assertQuerysetEqual(respnse.context["latest_questions_list"], [past_question])
        
    def test_two_question(self):
        """displaying multiple questions at the same time"""
        question1 = create_question("question1", 0, -5)
        question2 = create_question("question2", 0, -7)
        respnse = self.client.get(reverse("poll:index"))
        self.assertQuerysetEqual(respnse.context["latest_questions_list"], [question1,  question2])
        
    