from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from polls.models import *

def index(request):
    latest_questions_list = Question.objects.order_by("pub_date")[:5]
    context = { "latest_questions_list": latest_questions_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def result(request, question_id):
    return HttpResponse("You're looking at the results of the question %s" % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s" % question_id)
