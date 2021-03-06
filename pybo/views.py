from django.shortcuts import render
#---edit----
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
#from .models import QuestionAdmin
from .models import Question
from django.utils import timezone
from .forms import QuestionForm,AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
#---edit---

# Create your views here.

def index(request):
    # question_list=Question.objects.order_by('-create_date')
    # context={'question_list':question_list}
    
    page=request.GET.get('page','1')
    question_list=Question.objects.order_by('-create_date')
    paginator=Paginator(question_list,10)
    page_obj=paginator.get_page(page)

    context={'question_list':page_obj}
    return render(request,'pybo/question_list.html',context)

def detail(request,question_id):
    #question=Question.objects.get(id=question_id)
    question=get_object_or_404(Question,pk=question_id)
    context={'question':question}
    return render(request,'pybo/question_detail.html',context)

@login_required(login_url='commit:login')
def answer_create(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    #question.answer_set.create(content=request.POST.get('content'),create_date=timezone.now())
    if request.method=="POST":
        form=AnswerForm(request.POST)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.author=request.user
            answer.create_date=timezone.now()
            answer.question=question
            answer.save()
            return redirect('pybo:detail',question_id=question.id)
    else:
        form=AnswerForm()
    context={'question':question,'form':form}
    return render(request,'pybo/question_detail.html',context)
    #return redirect('pybo:detail',question_id=question.id)

@login_required(login_url='commit:login')
def question_create(request):
    # form=QuestionForm()
    # return render(request,'pybo/question_form.html',{'form':form})
    
    if request.method=='POST':
        form=QuestionForm(request.POST)
        if form.is_valid():
            question=form.save(commit=False)
            question.author=request.user
            question.create_date=timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form=QuestionForm()
    context={'form':form}
    return render(request,'pybo/question_form.html',context)