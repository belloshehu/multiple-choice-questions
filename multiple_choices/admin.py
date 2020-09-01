from django.contrib import admin
from django.contrib.admin import ModelAdmin   
from .models import Question, Choice, MultipleChoiceQuestion, AssessmentTaker


# Register your models here.

class QuestionAdmin(ModelAdmin):
    '''Question admin model'''
    list_filter = ['id']
    list_display = ['id', 'question_asked']
    ordering = ['id']

class MultipleChoiceQuestionAdmin(ModelAdmin):
    list_filter = ['id']
    list_display = ['id', 'title']
    ordering = ['id']

class ChoiceAdmin(ModelAdmin):
    list_filter = ['questions']
    list_display = ['questions_id', 'choice_statement']
    ordering = ['questions']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(AssessmentTaker)

admin.site.site_header = 'Multiple Choices Question Admin.'
