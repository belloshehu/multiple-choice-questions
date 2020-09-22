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
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
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
            if User.objects.filter(email=request.POST['email']).exists():
                messages.error(request, 'Username is already taken')
                return render(request, 'cbt/signup.html', {'form':form})
            form.save()
            user_detail = request.POST
            email_subject = 'Welcome to CBTMaker'
            message = f'''Hi {user_detail.get('username')}, 
                \n Thank you for registering with CBTMaker.
                \n\n Enjoy CBTMaker. \n\n CBTMaker team.'''
            email_sender = settings.EMAIL_HOST_USER
            recipient_list = [user_detail.get('email')]
            send_mail(email_subject, message, email_sender, recipient_list)
            print('Email sent')
            return redirect('cbt:home')
        else:
            return redirect(reverse('cbt:signup'))
    return render(request, 'cbt/signup.html', {'form':form})


def user_logout(request):
    logout(request)
    return redirect('cbt:home')


def cbt_list(request):
    ''' View for displaying list of CBTs. '''
    cbts = CBTAssessment.objects.filter(user=request.user.id)
    return render(request, 'cbt/cbt_list.html', {'cbts':cbts})


def password_reset(request):
    ''' View for resetting user's password. '''
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid:
            email = request.POST['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "cbt/password/password_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
				    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                    	return HttpResponse('Invalid header found.')
                    return redirect('password_reset_done')
    password_reset_form = PasswordResetForm()
    context = {'password_reset_form':password_reset_form}
    return render(request, 'cbt/password/password_reset.html', context)
    