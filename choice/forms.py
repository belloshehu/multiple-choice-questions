from django import forms
from .models import IndividualChoice, InstitutionChoice
from question.models import IndividualQuestion
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class IndividualChoiceForm(forms.ModelForm):
    choice_statement = forms.CharField(
        widget=forms.Textarea(attrs={'cols':50, 'rows':10}),
        help_text="enter the choice here",

    )
    is_correct = forms.BooleanField(
        help_text="indicate if this is the correct answer.",
        label="Is this the correct answer?"

    )
    class Meta:
        model = IndividualChoice
        exclude = ('question',)

    def save(self):
        if self.is_limit_exceeded() or self.is_existing() :
            return
        super().save()

    def is_existing(self):
        ''' Returns True is a Choice instance is already added.
            Otherwise it returns False.
        '''
        return IndividualChoice.objects.filter(
            choice_statement=self.instance.choice_statement,
            question_id=self.instance.question.id,
        ).exists()

    def is_limit_exceeded(self):
        return IndividualChoice.objects.filter(
            question_id=self.instance.question.id,
        ).count() >=  int(self.instance.question.no_of_choices)

    def get_number_of_choices(self):
        return IndividualQuestion.objects.get(
            id=self.instance.question.id,
        ).no_of_choices

    def get_related_choices(self):
        choices_objects = IndividualChoice.objects.filter(
            question_id=self.instance.question.id
        )
    def get_is_correct_vals(self, choices_objects):
        return [c_object.is_correct for c_object in choices_objects ]

    def get_choice_statement_vals(self, choices_objects):
        return [c_object.choice_statement for c_object in choices_objects ]

    def validate_choice(self, value):
        choice_objects = self.get_related_choices()
        if value in self.get_choice_statements(choice_objects):
            raise ValidationError(
                _('%(value)s is added already'),
                params={'value': value},
        )

class InstitutionChoiceForm(forms.ModelForm):

    class Meta:
        model = InstitutionChoice
        exclude = ('question',)
