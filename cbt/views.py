from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from cbt.forms import (PersonalCBTForm, PersonalQuestionForm, 
                        OrganisationalChoiceForm,
                        PersonalChoiceForm, OrganisationalChoiceForm,
                        InstitutionForm)
from multiple_choices.forms import UserRegistration, UserLogin
from .models import (CBTAssessment, InstitutionCBTAssessment,
                     OrganisationalCBT, PersonalCBT, Institution)

# Create your views here.


def home(request):
    return render (request, 'cbt/home.html')

def cbt_type(request):
    '''
    Handle CBT type selection.
    '''
    return render (request, 'cbt/ownership.html')


def create_cbt(request):
    '''
        Returns empty ComputerBasedTestForm form on GET request.
        Otherwise populated form is received.
    '''
    institution_form = InstitutionForm()
    cbt_form = PersonalCBTForm()
    if request.method == 'POST':
        if request.POST.get('type'):
            form = PersonalCBTForm()
            if form.is_valid:
                form.save()
                return redirect('cbt:cbt_ist')
    organisations = None
    cbts = None
    try:
        organisations = Institution.objects.all()
        cbts = PersonalCBT.objects.all()
    except (Institution.DoesNotExist, PersonalCBT.DoesNotExist):
       pass
    context = {'cbt_form':cbt_form, 'institution_form':institution_form,
                'organisations':organisations, 'cbts':cbts}
    return render(request, 'cbt/create_cbt.html', context)


def create_institution(request):
    '''
        Returns empty form for creating institution.
    '''
    if request.method == 'POST':
        form = InstitutionForm(request.POST)
        if form.is_valid:
            name = request.POST.get('name')
            form.save()
            messages.info(request, f'{name} added.')
    return redirect('cbt:create_cbt') 


def create_institution_cbt(request):
    form = PersonalCBTForm()
    if request.method == 'POST':
        form = PersonalCBTForm()
        if form.is_valid:
            form.save()
            return redirect('cbt:cbt_ist')
    return render(request, 'cbt/create_cbt.html', {'form':form})

def user_login(request):
    form = UserLogin()
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('cbt:cbt_list')
        messages.error(request, 'Login credentials error!')
        return redirect(reverse('cbt:login'))
    return render(request, 'cbt/login.html', {'form':form} )


def user_signup(request):
    form = UserRegistration()
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid:
            form.save()
            return redirect('cbt:home')
    return render(request, 'cbt/signup.html', {'form':form})


def user_logout(request):
    logout(request)
    return redirect('cbt:home')


def cbt_list(request):
    cbts = CBTAssessment.objects.filter(user=request.user.id)
    return render(request, 'cbt/cbt_list.html', {'cbts':cbts})