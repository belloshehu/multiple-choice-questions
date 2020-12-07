from django.db import models
from django.utils import timezone
from account.models import User


GRADES = [
        ('f', 'FAILED'),
        ('p', 'PASSED'),
]


class MultipleChoiceQuestion(models.Model):
    ''' Model for multiple choice questions. '''
    passage = models.TextField(max_length=3000,)
    title = models.CharField(max_length=50)
    duration = models.TimeField()
    no_of_questions = models.IntegerField(default=10)

    def __str__(self):
        return self.title


class Question(models.Model):
    ''' Model for questions to be asked with multiple choices.'''
    question_asked = models.CharField(max_length=200)
    grade = models.IntegerField(default=5)
    no_of_choices = models.IntegerField(default=4)
    multiple_choice_questions = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_asked


class Choice(models.Model):
    ''' Choice for each question asked. '''
    choice_statement = models.CharField(max_length=200, unique=True)
    is_correct = models.BooleanField(default=False)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_statement


class AssessmentTaker(models.Model):
    ''' Model for individuals taking the assessment. '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    status = models.CharField(choices=GRADES, max_length=20, default=GRADES[0])

    def __str__(self):
        return f'{self.user.username}'
