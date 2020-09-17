from django.contrib.auth.forms import UserModel
from django import forms
from cbt.models import (PersonalCBT, OrganisationalCBT, CBTAssessment,
                        PersonalChoice, OrganisationalChoice, 
                        PersonalQuestion, Question, Institution,
                        OrganisationalQuestion)

class PersonalCBTForm(forms.ModelForm):
    ''' Form for creating Personal CBT info .'''
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter CBT title', 'size':50}))
    description = forms.CharField(widget=forms.Textarea(attrs={'cols':100, 'rows':10, 'placeholder': 'Write what your cbt is all about?'}),)
    duration = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter duration in minutes', 'size':50}))
    candidates_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter number of candidates', 'size':50}))
    no_of_questions = forms.ChoiceField(widget=forms.NumberInput(attrs={'placeholder':'Number of questions', 'width':50}))
    

    class Meta:
        model = PersonalCBT
        fields = ('title', 'description', 'duration', 'candidates_no', 'no_of_questions')


class PersonalQuestionForm(forms.ModelForm):

    class Meta:
        model = PersonalQuestion
        fields = '__all__'


class OrganisationalQuestionForm(forms.ModelForm):

    class Meta:
        model = OrganisationalQuestion
        fields = '__all__'


class PersonalChoiceForm(forms.ModelForm):

    class Meta:
        model = PersonalChoice
        fields = '__all__'


class OrganisationalChoiceForm(forms.ModelForm):

    class Meta:
        model = OrganisationalChoice
        fields = '__all__'


class InstitutionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Institution name', 'size':50 }))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Institution address', 'size':70}))

    class Meta:
        model = Institution
        fields = '__all__'
