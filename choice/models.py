from django.db import models
from django.shortcuts import reverse
from question.models import IndividualQuestion, InstitutionQuestion

class Choice(models.Model):
    ''' Choice for each question asked.
        This model is abstract as it is not intended to be instantiated.
     '''
    choice_statement = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.choice_statement


class IndividualChoice(Choice):
    ''' Represents choice in assessment created by individual. '''
    question = models.ForeignKey(IndividualQuestion, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('choice:individual-detail', kwargs={'pk':self.id})


class InstitutionChoice(Choice):
    ''' Represents choice in assessment created by Institution. '''
    question = models.ForeignKey(InstitutionQuestion, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('choice:institution-detail', kwargs={'pk':self.id})
