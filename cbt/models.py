from django.db import models
from django.utils import timezone
from account.models import User
from django.shortcuts import reverse


GRADES = [
        ('f', 'FAILED'),
        ('p', 'PASSED')
]

class Institution(models.Model):
    '''
    Institution that a CBT might belong to.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Name of your Institution')
    address = models.CharField(max_length=150, verbose_name='Address of your Institution')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cbt:institution-details', kwargs={'pk':self.id})


class PersonalCBT(models.Model):
    '''
        Represent CBT for individuals such as parents,
        teachers etc.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=1000, null=True)
    start_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_date = models.DateField(null=True)
    end_time = models.TimeField(null=True)
    duration = models.IntegerField(null=True)
    candidates_no = models.IntegerField(default=10, null=True)
    no_of_questions = models.IntegerField(default=10, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cbt:individual-assessment-detail', kwargs={'pk':self.id})


class OrganisationalCBT(PersonalCBT):
    '''
        Represent CBT for organisation such as school,
        company etc.
    '''
    organisation = models.ForeignKey(Institution, on_delete=models.CASCADE)


    def __str__(self):
        return self.title


class Question(models.Model):
    ''' Model for questions to be asked with multiple choices.'''
    question_asked = models.TextField(unique=True)
    grade = models.IntegerField(default=5)
    no_of_choices = models.IntegerField(default=4)


    def __str__(self):
        return self.question_asked


class PersonalQuestion(Question):
    ''' Represents questions in personal CBT. '''
    personal_cbt = models.ForeignKey(PersonalCBT, on_delete=models.CASCADE)


class OrganisationalQuestion(Question):
    ''' Represents questions in organisational CBT. '''
    organisational_cbt = models.ForeignKey(OrganisationalCBT, on_delete=models.CASCADE)


class Choice(models.Model):
    ''' Choice for each question asked. '''
    choice_statement = models.TextField(unique=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_statement


class PersonalChoice(Choice):
    ''' Represents choice in personal CBT questions. '''
    questions = models.ForeignKey(PersonalQuestion, on_delete=models.CASCADE)


class OrganisationalChoice(Choice):
    ''' Represents choice in organisational CBT questions. '''
    questions = models.ForeignKey(PersonalQuestion, on_delete=models.CASCADE)


class CBTAssessment(models.Model):
    ''' Model for individuals taking the assessment. '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    status = models.CharField(choices=GRADES, max_length=20, default=GRADES[0])
    cbt = models.ForeignKey(PersonalCBT, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class InstitutionCBTAssessment(CBTAssessment):
    ''' Assessment for Instituions .'''
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
