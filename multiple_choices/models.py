from django.db import models
from django.utils import timezone
from django.contrib.auth .models import User


# Create your models here.



class MultipleChoiceQuestion(models.Model):
    ''' Model for multiple choice questions. '''
    passage = models.TextField(max_length=500)
    title = models.CharField(max_length=20)
    duration = models.TimeField()
    no_of_questions = models.IntegerField(default=10)

    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Question(models.Model):
    ''' Model for questions to be asked with multiple choices.'''
    question_asked = models.CharField(max_length=100)
    grade = models.IntegerField(default=5)
    no_of_choices = models.IntegerField(default=4)
    multiple_choice_questions = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_asked


class Choice(models.Model):
    ''' Choice for each question asked. '''
    choice_statement = models.CharField(max_length=100, unique=True)
    is_correct = models.BooleanField(default=False)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_statement



class AssessmentTaker(models.Model):
    ''' Model for individuals taking the assessment. '''
    GRADES = [
        ('f', 'FAILED'),
        ('p', 'PASSED')
    ]
    username = models.CharField(unique=True, max_length=20)
    score = models.IntegerField(default=0)
    status = models.CharField(choices=GRADES, max_length=20)

    def __str__(self):
        return f'{self.username}'