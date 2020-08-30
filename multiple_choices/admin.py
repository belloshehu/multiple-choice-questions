from django.contrib import admin
from .models import Question, Choice, MultipleChoiceQuestion, AssessmentTaker


# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(AssessmentTaker)

admin.site.site_header = 'Multiple Choices Question Admin.'
