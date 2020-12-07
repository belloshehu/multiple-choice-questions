from django.shortcuts import (
                    render,
                    redirect,
                    reverse,
                    get_object_or_404,
                    get_list_or_404,
                )
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from cbt.forms import (
                    IndividualAssessmentForm,
                    InstitutionForm, InstitutionAssessmentForm
                    )
from multiple_choices.forms import UserRegistration, UserLogin
from .models import (
                    InstitutionAssessment,
                    IndividualAssessment,
                    Institution
                    )
from choice.models import IndividualChoice, InstitutionChoice
from question.models import IndividualQuestion, InstitutionQuestion
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
    '''Renders Assessment types template'''
    return render (request, 'cbt/assessment_types.html')


class AssessmentHelpView(TemplateView):
    template_name = 'cbt/partials/assessment_help.html'

###############
# Institution Assessment type CRUD, list and details views:
##############


class InstitutionAssessmentCreateView(LoginRequiredMixin ,CreateView):
    ''' View to create Assessment by organisation. '''
    model = InstitutionAssessment
    form_class = InstitutionAssessmentForm
    template_name = 'cbt/institution/assessment_form.html'
    success_url = reverse_lazy('cbt:institution-assessment-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class InstitutionAssessmentListView(LoginRequiredMixin, ListView):
    model = InstitutionAssessment
    template_name = 'cbt/institution/assessment_list.html'
    context_object_name = 'assessments'

class InstitutionAssessmentDetailView(LoginRequiredMixin, DetailView):
    model = InstitutionAssessment
    template_name = 'cbt/institution/assessment_detail.html'
    context_object_name = 'assessment'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            context['choices'] = InstitutionChoice.objects.all()
            context['questions'] = InstitutionQuestion.objects.filter(
                assessment_id=self.kwargs.get('pk')
            )
        except InstitutionChoice.DoesNotExist:
            context['choices'] = None
        except InstitutionQuestion.DoesNotExist:
             context['questions'] = None
        return context

class InstitutionAssessmentUpdateView(LoginRequiredMixin, UpdateView):
    model = InstitutionAssessment
    form_class = InstitutionAssessmentForm
    template_name = 'cbt/institution/assessment_update_form.html'
    success_url = reverse_lazy('cbt:institution-assessment-list')
    context_object_name = 'assessment'


class InstitutionAssessmentDeleteView(LoginRequiredMixin, DeleteView):
    model = InstitutionAssessment
    form_class = InstitutionAssessmentForm
    template_name = 'cbt/institution/assessment_delete_confirm.html'
    success_url = reverse_lazy('cbt:institution-assessment-list')
    context_object_name = 'assessment'


# ####################
# Individual assessment CRUD, details and list views:
######################

class IndividualAssessmentCreateView(LoginRequiredMixin ,CreateView):
    ''' View to create Assessment by individuals. '''
    model = IndividualAssessment
    form_class = IndividualAssessmentForm
    template_name = 'cbt/individual/individual_assessment.html'
    success_url = reverse_lazy('cbt:individual-assessment-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IndividualAssessmentListView(LoginRequiredMixin, ListView):
    model = IndividualAssessment
    template_name = 'cbt/individual/individual_assessment_list.html'
    context_object_name = 'assessments'

    def get_queryset(self):
        try:
            queryset = IndividualAssessment.objects.filter(
                user=self.request.user
            )
        except IndividualAssessment.DoesNotExist:
            pass
        return queryset

class IndividualAssessmentDetailView(LoginRequiredMixin, DetailView):
    model = IndividualAssessment
    template_name = 'cbt/individual/individual_assessment_detail.html'
    context_object_name = 'assessment'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            context['choices'] = IndividualChoice.objects.filter(
                question__assessment__user=self.request.user
            )
            context['questions'] = IndividualQuestion.objects.filter(
                assessment_id=self.kwargs.get('pk'),
                assessment__user=self.request.user
            )
        except IndividualChoice.DoesNotExist:
            context['choices'] = None
        except IndividualQuestion.DoesNotExist:
            context['questions'] = None
        return context


    def get_question_with_passage(self):
        Q1 = Q(passage__title=None)
        Q2 = Q(passage__body=None)
        Q3 = Q(passage__no_of_questions=None)
        question_with_passage = None
        try:
            question_with_passage = IndividualQuestion.objects.filter(
                Q1&Q2&Q3
            )
        except IndividualQuestion.DoesNotExist:
            pass
        return question_with_passage


class IndividualAssessmentDeleteView(LoginRequiredMixin, DeleteView):
    model = IndividualAssessment
    form_class = IndividualAssessmentForm
    template_name = 'cbt/individual/assessment_confirm_delete.html'
    success_url = reverse_lazy('cbt:individual-assessment-list')
    context_object_name = 'assessment'


class IndividualAssessmentUpdateView(LoginRequiredMixin, UpdateView):
    model = IndividualAssessment
    form_class = IndividualAssessmentForm
    template_name = 'cbt/individual/assessment_update_form.html'
    success_url = reverse_lazy('cbt:individual-assessment-list')
    context_object_name = 'assessment'


#================================
# Sample Assessments
#===============================


class SampleAssessmentListView(LoginRequiredMixin, ListView):
    model = IndividualAssessment
    template_name = 'cbt/sample/sample_list.html'
    context_object_name = 'assessments'
    def get_queryset(self):
        try:
            queryset = IndividualAssessment.objects.filter(
                user__is_superuser=True,
                is_sample=True
            )
        except IndividualAssessment.DoesNotExist:
            pass
        return queryset


#=========================
# Institution CRUD, list and details views
#==========================


class InstitutionListView(LoginRequiredMixin, ListView):
    model = Institution
    template_name = 'cbt/institution_list.html'
    context_object_name = 'institutions'

    def get_queryset(self):
        try:
            queryset = Institution.objects.filter(
                user=self.request.user
            )
        except Institution.DoesNotExist:
            pass
        return queryset


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
