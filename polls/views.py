from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from .forms import Survey,Choiceform
# Create your views here.
from .models import Question, Choice
from django.contrib import messages

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
         return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        """
        #return Question.objects.all()[:5]
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def CreateQuestion(request):
    if request.method=="POST":
        form=Survey(request.POST)
        form1=Choiceform(request.POST)
        if form.is_valid():
            form.save()
            question=Question.objects.filter(question_text=request.POST['question_text']).first()
            question.choice_set.create(choice_text=request.POST['choice_text1'])
            question.choice_set.create(choice_text=request.POST['choice_text2'])
            messages.success(request,f'question created succesfully')
            return redirect('/polls/home/')
    else:
        form = Survey()
        form1=Choiceform()
    return render(request, 'polls/question_form.html', {'form': form,'form1':form1})
