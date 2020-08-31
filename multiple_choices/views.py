from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AssessmentForm, UserRegistration, UserLogin
from .models import AssessmentTaker, MultipleChoiceQuestion, Question, Choice
# Create your views here.


def home(request):
    ''' View for assessment taking. '''
    return render(request, 'multiple_choices/home.html')


def register(request):
    ''' View to handle user registration.'''
    form = UserRegistration()
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid:
            try:
                form.save(commit=True)
                return render(request, 'multiple_choices/registration_success.html', {'form':form})
            except ValueError:
                pass
        messages.warning(request, 'Wrong information entered!')
        return redirect(reverse('multiple_choices:register'))
    return render(request, 'multiple_choices/register.html', {'form':form})


def user_login(request):
    ''' View to handle user login.'''
    form = UserLogin()
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('multiple_choices:home')
        else:
            messages.info(request, 'username or password or both are incorrect.')
            return redirect(reverse('multiple_choices:login'))
    return render(request, 'multiple_choices/login.html', {'form':form})


def user_logout(request):
    ''' view function to logout user. '''
    logout(request)
    return redirect('multiple_choices:home')


def assessment(request):
    ''' View for taking assessment page. '''
    questions, choices = None, None
    multiple_choice_questions = None
    if request.user.is_authenticated: 
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
        context = {
            'multiple_choice_questions':multiple_choice_questions,
            'questions':questions,
            'choices':choices,
            'duration': 10,
            }
        return render(request, 'multiple_choices/assessment.html', context)
    return redirect('multiple_choices:login')


def process_result(request):
    '''View to compute assessment result. '''
    score = 0
    passed = False
    total_mark = 0
    if request.method == 'POST':
        mark_per_question = 0
        for key in list(request.POST.keys())[1:]:
            choice_id = request.POST.get(key, None)
            print(choice_id)
            choice = Choice.objects.get(id=int(choice_id))
            if choice.is_correct:
                # get the score assigned to the question 
                mark_per_question = Question.objects.get(id=choice.questions.id).grade
                score+= mark_per_question
        # calculate grade score
        total_questions = len(list(request.POST.keys()))-1
        total_mark = total_questions * mark_per_question
        try:
            percentage = score * 100 / total_mark
        except ZeroDivisionError:
            percentage = 0
        if percentage >= 75:
            passed = True
        return render(request, 'multiple_choices/result.html', {'score': score, 'grade': passed})
    return redirect('multiple_choices:home')
    