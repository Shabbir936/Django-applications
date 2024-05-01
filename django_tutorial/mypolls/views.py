from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Question


# Create your views here.


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request,"mypolls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "mypolls/detail.html", {"question": question})


def results(request, question_id):
    response = f"You're looking at the response for the question {question_id}"
    return HttpResponse(response)


def vote(request, question_id):
    response = f"You're voting for the questions {question_id}"
    return HttpResponse(response)
