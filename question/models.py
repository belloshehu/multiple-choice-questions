from django.db import models
from django.shortcuts import reverse
from cbt.models import IndividualAssessment, InstitutionAssessment


class QuestionPassage(models.Model):
    ''' Abstract model for Passage to answer questions from.
        This is used if the questions come from a passage.
        It is therefore optional.
    '''
    title = models.CharField(max_length=50, null=True, blank=True)
    body = models.TextField(max_length=500, null=True, blank=True)
    # number of questions to be asked from the passage.
    no_of_questions = models.IntegerField(default=4, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

class IndividualQuestionPassage(QuestionPassage):
    assessment = models.ForeignKey(
        IndividualAssessment,
        on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse(
            'question:individual-passage-detail',
            kwargs={'pk':self.id}
        )

    def get_delete_url(self):
        return reverse(
            'question:individual-passage-delete',
            kwargs={'pk':self.id}
        )

    def get_update_url(self):
        return reverse(
            'question:individual-passage-update',
            kwargs={'pk':self.id})

    def get_list_url(self):
        return reverse('question:individual-passage-list')


class InstitutionQuestionPassage(QuestionPassage):
    assessment = models.ForeignKey(
        InstitutionAssessment,
        on_delete=models.CASCADE
    )
    def get_absolute_url(self):
        return reverse(
            'question:institution-passage-detail',
            kwargs={'pk':self.id}
        )

    def get_delete_url(self):
        return reverse(
            'question:institution-passage-delete',
            kwargs={'pk':self.id}
        )

    def get_update_url(self):
        return reverse(
            'question:institution-passage-update',
            kwargs={'pk':self.id})

    def get_list_url(self):
        return reverse('question:institution-passage-list')


class Question(models.Model):
    ''' Model for questions to be asked with multiple choices.'''
    question_asked = models.TextField(unique=True)
    score = models.IntegerField(default=5)
    no_of_choices = models.IntegerField(default=4)

    def __str__(self):
        return self.question_asked
    class Meta:
        abstract = True


class IndividualQuestion(Question):
    ''' Represents questions in personal CBT. '''
    passage = models.ForeignKey(IndividualQuestionPassage, on_delete=models.CASCADE)
    assessment = models.ForeignKey(IndividualAssessment, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('question:individual-detail', kwargs={'pk:self.id'})


class InstitutionQuestion(Question):
    ''' Represents questions in organisational CBT. '''
    passage = models.ForeignKey(InstitutionQuestionPassage, on_delete=models.CASCADE)
    assessment = models.ForeignKey(InstitutionAssessment, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('question:institutional-detail', kwargs={'pk:self.id'})
