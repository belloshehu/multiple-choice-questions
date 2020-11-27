from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from cbt.forms import (
                    PersonalCBTForm, PersonalQuestionForm,
                    OrganisationalChoiceForm,
                    PersonalChoiceForm, OrganisationalChoiceForm,
                    InstitutionForm, OrganisationalCBTForm
                    )
from multiple_choices.forms import UserRegistration, UserLogin
from .models import (
                    CBTAssessment, InstitutionCBTAssessment,
                    OrganisationalCBT, PersonalCBT, Institution
                    )
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.generic import(
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def home(request):
    return render (request, 'cbt/home.html')

def cbt_type(request):
    '''
    Handle CBT type selection.
    '''
    return render (request, 'cbt/ownership.html')
class AssessmentHelpView(TemplateView):
    template_name = 'cbt/partials/assessment_help.html'

###############
# Organisation Assessment CRUD
##############
class OrganisationAssessmentCreateView(LoginRequiredMixin ,CreateView):
    ''' View to create Assessment by organisation. '''
    model = OrganisationalCBT
    form_class = OrganisationalCBTForm
    template_name = 'cbt/organisation_assessment_form.html'
    success_url = reverse_lazy('cbt:cbt_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class IndividualAssessmentListView(LoginRequiredMixin, ListView):
    model = PersonalCBT
    template_name = 'cbt/cbt_list.html'
    context_object_name = 'assessments'

# ####################
# Individual assessment CRUD:
######################

class IndividualAssessmentCreateView(LoginRequiredMixin ,CreateView):
    ''' View to create Assessment by individuals. '''
    model = PersonalCBT
    form_class = PersonalCBTForm
    template_name = 'cbt/individual_assessment.html'
    success_url = reverse_lazy('cbt:cbt_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IndividualAssessmentDetailView(LoginRequiredMixin, DetailView):
    model = PersonalCBT
    template_name = 'cbt/individual_assessment_detail.html'
    context_object_name = 'assessment'

class InstitutionListView(LoginRequiredMixin, ListView):
    model = Institution
    template_name = 'cbt/institution_list.html'
    context_object_name = 'institutions'


class InstitutionDetailView(LoginRequiredMixin, DetailView):
    pass

class InstitutionDeleteView(LoginRequiredMixin, DeleteView):
    model = Institution
    template_name = 'cbt/institution_confirm_delete.html'
    success_url = reverse_lazy('cbt:institution-list')


class InstitutionUpdateView(LoginRequiredMixin, UpdateView):
    model = Institution
    form_class = InstitutionForm
    template_name = 'cbt/institution_update_form.html'
    success_url = reverse_lazy('cbt:institution-list')


class InstitutionCreateView(LoginRequiredMixin, CreateView):
    ''' View to create instance of Institution.'''
    model = Institution
    form_class = InstitutionForm
    template_name = 'cbt/institution_form.html'
    success_url = reverse_lazy('cbt:institution-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

"""
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
"""

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
