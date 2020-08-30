from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import AssessmentForm
from .models import AssessmentTaker
# Create your views here.


def home(request):
    ''' View for assessment taking. '''
    return render(request, 'multiple_choices/home.html')


def register(request):
    pass

def assessment(request):
    pass