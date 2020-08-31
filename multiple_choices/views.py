from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import AssessmentForm
from .models import AssessmentTaker, MultipleChoiceQuestion, Question, Choice
# Create your views here.


def home(request):
    ''' View for assessment taking. '''
    return render(request, 'multiple_choices/home.html')


def register(request):
    pass


def assessment(request):
    score = 0
    questions, choices = None, None
    multiple_choice_questions = None
    if request.method == 'GET':
        try:
            multiple_choice_questions = MultipleChoiceQuestion.objects.all() 
            questions = Question.objects.all()
            choices = Choice.objects.all()
        except MultipleChoiceQuestion.DoesNotExist:
            pass
        except Question.DoesNotExist:
            pass
        except Choice.DoesNotExist:
            pass
    else:
        return redirect('multiple_choices:result')
    context = {
        'multiple_choice_questions':multiple_choice_questions,
        'questions':questions,
        'choices':choices,
        }
    return render(request, 'multiple_choices/assessment.html', context)


def process_result(request):
    pass