from typing import Any
from django.utils import timezone
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.db.models import F
from django.views import generic


# Create your views here.


class IndexView(generic.ListView):
    template_name = "mypolls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self) -> QuerySet[Any]:
        """Return the last five published questions (not including those to be
        published in the)

        Returns:
            QuerySet[Any]: List of 5 Questions in descending of published date
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "mypolls/detail.html"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    


class ResultsView(generic.DetailView):
    model = Question
    template_name = "mypolls/results.html"


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "mypolls/detail.html",
            {"question": question, "error_message": "You didnt select a choice"},
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("mypolls:results", args=(question.id,)))
