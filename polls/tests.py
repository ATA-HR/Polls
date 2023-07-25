from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import *

def create_question(question_text="question",
        days=0, hours=0, minutes=0, seconds=0):
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
    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the\
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_questions_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on\
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_questions_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions\
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question("Future question.", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_questions_list"],
            [question],
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_questions_list"],
            [question2, question1],
        )

    def test_questions_with_choice(self):
        """Quetsions with choice(s) will be published on the site"""
        question = create_question(hours=-5)
        question.choice_set.create(choice_text="choice", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_questions_list"], [question])

    def test_questions_with_no_choice(self):
        """Quetsions with no choice(s) will NOT be published on the site"""
        question = create_question(hours=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions_list"], [])

class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        """Questions with pub_date in the past displyed in detail page"""
        question = create_question("past_question", -22)
        response = self.client.get(reverse("polls:detail", args=(question.id, )))
        self.assertContains(response, question.question_text)
    
    def test_future_question(self):
        """
        Questions with pub_date in the future not displyed in detail page\
        and returns a page not found 404.
        """
        question = create_question("future_question", 33)
        url = reverse("polls:detail", args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
