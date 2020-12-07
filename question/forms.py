from django import forms
from .models import (
    IndividualQuestion,
    InstitutionQuestion,
    IndividualQuestionPassage
)

class IndividualQuestionPassageForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(attrs={'cols':100, 'rows':20})
    )
    class Meta:
        model = IndividualQuestionPassage
        fields = ('title', 'body', 'no_of_questions')


class IndividualQuestionForm(forms.ModelForm):
    question_asked = forms.CharField(
        label='Question statement',
        widget=forms.Textarea(attrs={'cols':100, 'rows':10})
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
        exclude = ('assessment', 'passage')


class InstitutionQuestionForm(forms.ModelForm):

    class Meta:
        model = InstitutionQuestion
        exclude = ('assessment','passage')
