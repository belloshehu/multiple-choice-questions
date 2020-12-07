from django.contrib import admin
from .models import (
    IndividualAssessment,
    InstitutionAssessment,
    Institution
)

# Register your models here.
admin.site.register(IndividualAssessment)
admin.site.register(InstitutionAssessment)
admin.site.register(Institution)