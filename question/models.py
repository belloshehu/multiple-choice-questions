from django.db import models
from django.shortcuts import reverse
from cbt.models import PersonalCBT, OrganisationalCBT


class Question(models.Model):
    ''' Model for questions to be asked with multiple choices.'''
    question_asked = models.CharField(max_length=200, unique=True)
    score = models.IntegerField(default=5)
    no_of_choices = models.IntegerField(default=4)


    def __str__(self):
        return self.question_asked
    class Meta:
        abstract = True


class IndividualQuestion(Question):
    ''' Represents questions in personal CBT. '''
    assessment = models.ForeignKey(PersonalCBT, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('question:individual-detail', kwargs={'pk:self.id'})


class InstitutionQuestion(Question):
    ''' Represents questions in organisational CBT. '''
    assessment = models.ForeignKey(OrganisationalCBT, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('question:institutional-detail', kwargs={'pk:self.id'})
