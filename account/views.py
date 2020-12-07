from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    View,
    TemplateView
)
from django.contrib.auth import(
    authenticate,
    login,
    logout,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from account.models import User
from django.conf import settings
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView as CorePasswordResetView
from cbt.models import IndividualAssessment, InstitutionAssessment

class UserRegistrationView(View):

    template_name = 'account/registration_form.html'
    def get(self, request):
        form = UserRegistrationForm
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=request.POST['email']).exists():
                messages.error(request, 'Username is already taken')
                return render(request, self.template_name, {'form':form})
            form.save()
            user_detail = request.POST
            email_subject = 'Welcome to CBTMaker'
            message = f'''Hi {user_detail.get('username')},
                \n Thank you for registering with CBTMaker.
                \n\n Enjoy CBTMaker. \n\n CBTMaker team.'''
            email_sender = settings.EMAIL_HOST_USER
            recipient_list = [user_detail.get('email')]
            send_mail(email_subject, message, email_sender, recipient_list)
            return redirect('cbt:home')
        else:
            return render(request, self.template_name, {'form':form})


class UserLoginView(View):
    form = UserLoginForm
    template_name = 'account/login_form.html'
    def get(self, request):
        return render(request, self.template_name, {'form':self.form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('cbt:home')
            else:
                messages.error(request, 'Either username or password is incorrect!')
        return render(request, self.template_name, {'form':form})

def user_login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('cbt:cbt_list')
        messages.error(request, 'Login credentials error!')
        return redirect(reverse('cbt:login'))
    return render(request, 'cbt/login.html', {'form':form} )




class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('cbt:home')

class PasswordResetView(CorePasswordResetView):
    template_name =  'account/password/password_reset.html'

    def get(self, request):
        form = PasswordResetForm()
        return render(request, self.template_name, {'password_reset_form':form})

    def post(self, request):
        ''' View for resetting user's password. '''
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "account/password/password_email.txt"
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
                        send_mail(subject, email, settings.DEFAUL_FROM_EMAIL, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('password_reset_done')
        context = {'password_reset_form':form}
        return render(request, self.template_name, context)


#========================
#    Dashboard views
#========================

class DashboardView(LoginRequiredMixin, TemplateView):
    ''' View to render dashboard page.'''
    template_name = 'account/dashboard/dashboard.html'
    context = {}

    def get(self, request):
        context = self.get_assessment_objects(request)
        return render(request, self.template_name, context )

    def get_assessment_objects(self, request):
        try:
            self.context['institution_assessments'] = InstitutionAssessment.objects.filter(
                user_id=request.user.id
            )
            self.context['individual_assessments'] = IndividualAssessment.objects.filter(
                user_id=request.user.id
            )
        except InstitutionAssessment.DoesNotExist:
            self.context['institution_assessments'] = None
        except IndividualAssessment.DoesNotExist:
            self.context['individual_assessments'] = None
        return self.context


class UserAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = (
        'first_name',
        'last_name',
        'middle_name',
        'username',
    )
    template_name = 'account/account_update_form.html'
    success_url = reverse_lazy('account:dashboard')
