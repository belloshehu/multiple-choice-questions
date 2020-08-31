from django import forms
from .models import MultipleChoiceQuestion

class AssessmentForm(forms.ModelForm):
    ''' Form for the assessment including questions and choices.'''
    
    class Meta:
        model = MultipleChoiceQuestion
        exclude = ['no_of_questions']

