from django.shortcuts import render,get_object_or_404
from django.http import Http404,HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.
from .models import Question,Choice
def index(request):
	latest_question_list=Question.objects.order_by('-pub_date')[:5]
	return render(request,'polls/index.html',{'latest_question_list':latest_question_list})
	
def detail(request, question_id):
	try:
		question = get_object_or_404(Question, pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	print('question-',question.choice_set.all())
	return render(request, 'polls/detail.html', {'question': question})
	
def vote(request,question_id):
	question=get_object_or_404(Question,pk=question_id)
	try:
		selected_choice=question.choice_set.get(pk=request.POST['choice'])
	except(KeyError,Choice.DoesNotExist):
		return render(request,'polls/detail.html',{'question':question,'error_message':'You didn\'t select a choice.'})
	else:
		selected_choice.votes+=1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
		
def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})