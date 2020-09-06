from django import forms
from .models import MultipleChoiceQuestion
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth.models import User

class AssessmentForm(forms.ModelForm):
    ''' Form for the assessment including questions and choices.'''
    
    class Meta:
        model = MultipleChoiceQuestion
        exclude = ['no_of_questions']


class UserRegistration(UserCreationForm):
    """Customer registration."""
    username = forms.CharField(
        max_length=100, required=True, help_text='', label='',
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    first_name = forms.CharField(
        max_length=100, required=True, help_text="", label='',
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=100, required=True, help_text="", label='',
        widget=forms.TextInput(attrs={'placeholder': 'Second name'})
    )
    email = forms.EmailField(
        max_length=250, required=True, help_text="", label='',
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )
    
    password1 = forms.CharField(
        max_length=250, required=True, help_text="", label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        max_length=250, required=True, help_text="", label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'})
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'password1', 'password2',)


class UserLogin(forms.Form):
    '' 'User login form. '''
    username = forms.CharField(
        max_length=100, required=True, help_text='', label='',
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        max_length=250, required=True, help_text="", label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
   

class MultipleChoiceQuestionForm(forms.ModelForm):
    '''Create form for creating Multiple choice questions.
    '''
    
    class Meta:
        model = MultipleChoiceQuestion
        fields = ('passage', 'title', 'duration', 'no_of_questions')
    