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

class BaseAbstractAssessment(models.Model):
    ''' Abstract model class for creating all sorts of assessment.'''
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
    is_sample = models.BooleanField(default=False, null=True)
    # urls for detail, delete and update
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delete_url = None
        self.update_url = None
        self.absolute_url = None
        self.list_url = None


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(self.absolute_url, kwargs={'pk':self.id})

    def get_delete_url(self):
        return reverse(self.delete_url, kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse(self.update_url, kwargs={'pk':self.id})

    def get_list_url(self):
        return reverse(self.list_url)


    class Meta:
        abstract = True


class IndividualAssessment(BaseAbstractAssessment):
    '''
        Represent assessments for individuals such as parents,
        teachers etc.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delete_url = 'cbt:individual-assessment-delete'
        self.update_url = 'cbt:individual-assessment-update'
        self.absolute_url = 'cbt:individual-assessment-detail'
        self.list_url = 'cbt:individual-assessment-list'


class InstitutionAssessment(BaseAbstractAssessment):
    '''
        Represent assessments for organisation such as school,
        company etc.
    '''
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delete_url = 'cbt:institution-assessment-delete'
        self.update_url = 'cbt:institution-assessment-update'
        self.absolute_url = 'cbt:institution-assessment-detail'
        self.list_url = 'cbt:institution-assessment-list'


class IndividualAssessmentTaker(models.Model):
    ''' Model for individuals taking theIndividual assessment type. '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    status = models.CharField(choices=GRADES, max_length=20, default=GRADES[0])
    assessment = models.ForeignKey(IndividualAssessment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class InstitutionAssessmentTaker(IndividualAssessment):
    ''' Model for individual taking Insitution Assessment type .'''
    assessment = models.ForeignKey(InstitutionAssessment, on_delete=models.CASCADE)
