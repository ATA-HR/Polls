# coding: utf-8
from polls.models import *
Question.objects.all()
Question.objects.all()[0\]
Question.objects.all()[0]
q = Question.objects.all()[0]
q.pub_date
q.fe
q.was_published_recently()
Question(queston_text="old_question", pub_date=timzone.now()-365)
from django.utils import timezone
Question(queston_text="old_question", pub_date=timzone.now()-365)
Question(queston_text="old_question", pub_date=timezone.now()-365)
from datetime import timedelta
Question(queston_text="old_question", pub_date=timezone.now()-timedelta(days=365))
Question(question_text="old_question", pub_date=timezone.now()-timedelta(days=365))
Question.objects.all()
