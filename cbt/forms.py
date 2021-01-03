from django.contrib.auth.forms import UserModel
from django import forms
from django.utils import timezone
from cbt.models import (
        IndividualAssessment,
        InstitutionAssessment,
        Institution,
    )

class IndividualAssessmentForm(forms.ModelForm):
    ''' Form for creating Personal CBT info. .'''
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':'Enter CBT title', 'size':50}
            )
        )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'cols':100, 'rows':10, 'placeholder': 'Write what your cbt is all about?'}
            ),

        )
    start_date = forms.DateField(
         label='Starting date(Date assessment will be available.)',
        widget=forms.DateInput(
            attrs={'placeholder':'Date to start', 'type':'date'}
            ),
        initial=timezone.datetime.today(),
        error_messages={'invalid':'invalid'}
         )
    start_time = forms.TimeField(
        label='Starting time(Time assessment will be available.)',
        widget=forms.TimeInput(
            attrs={'placeholder':'Time to start', 'type':'time'}
            ),
        initial=timezone.datetime.now(),
        error_messages={'invalid':'invalid'}
        )
    end_date = forms.DateField(
        label='Closing date(Date assessment will be unavailable.)',
        widget=forms.DateInput(
            attrs={'placeholder':'Date to end', 'type':'date'}
            ),
        error_messages={'invalid':'invalid'}
        )
    end_time = forms.TimeField(
        label='Closing time(Time assessment will be unavailable.)',
        widget=forms.TimeInput(
            attrs={'placeholder':'Time to expire', 'type':'time'}
            ),
        help_text='Time to end Assessment',
        error_messages={'invalid':'invalid'}
        )
    duration = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'placeholder':'Enter duration in minutes',}
            ),
        error_messages={'invalid':'invalid'}
        )
    candidates_no = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'placeholder':'Enter number of candidates',}
            ),
        error_messages={'invalid':'invalid'}
        )
    no_of_questions = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'placeholder':'Number of questions'}
            ),
        error_messages={'invalid':'invalid'}

        )


    class Meta:
        model = IndividualAssessment
        fields = (
            'title',
            'description',
            'duration',
            'candidates_no',
            'no_of_questions',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'is_sample'
        )

class InstitutionAssessmentForm(IndividualAssessmentForm):

    class Meta:
        model = InstitutionAssessment
        exclude = ('user',)

class InstitutionForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Institution name', 'size':50 }
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Institution address', 'size':70}
        )
    )

    class Meta:
        model = Institution
        fields = ('name', 'address')
