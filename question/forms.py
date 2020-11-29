from django import forms
from .models import IndividualQuestion, InstitutionQuestion


class IndividualQuestionForm(forms.ModelForm):
    question_asked = forms.CharField(
        label='Question statement',
    )
    score = forms.IntegerField(
        label='Score to be earned',
        widget=forms.NumberInput()
    )
    no_of_choices = forms.IntegerField(
        label='Number of choices',
        widget=forms.NumberInput()
    )

    class Meta:
        model = IndividualQuestion
        exclude = ('assessment',)


class InstitutionQuestionForm(forms.ModelForm):

    class Meta:
        model = InstitutionQuestion
        exclude = ('assessment',)
