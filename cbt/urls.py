from django.urls import path
from . import views
from multiple_choices.views import sample
from django.contrib.auth import urls

app_name = 'cbt'
urlpatterns = [
    path('', views.home, name='home'),
    path('assessment-types', views.cbt_type, name='cbt_type'),
    path(
        'institution-detail/<int:pk>/',
        views.InstitutionDetailView.as_view(),
        name='institution-detail'
    ),
    path(
        'create-institution/',
        views.InstitutionCreateView.as_view(),
        name='create_institution'
    ),

    path(
        'institution-list/',
        views.InstitutionListView.as_view(),
        name='institution-list'
    ),
    path(
        'institution-update/<int:pk>/',
        views.InstitutionUpdateView.as_view(),
        name='institution-update'
    ),
    path(
        'institution-delete/<int:pk>/',
        views.InstitutionDeleteView.as_view(),
        name='institution-delete'
    ),
    path('sample/', sample, name='sample'),
    # Individual assessment type url
    path(
        'create-individual-assessment/',
        views.IndividualAssessmentCreateView.as_view(),
        name='create-individual-assessment'
    ),
    path(
        'individual-assessment-list/',
        views.IndividualAssessmentListView.as_view(),
        name='individual-assessment-list'
    ),
    path(
        'individual-assessment-detail/<int:pk>/',
        views.IndividualAssessmentDetailView.as_view(),
        name='individual-assessment-detail'
    ),
    path(
        'individual-assessment-delete/<int:pk>/',
        views.IndividualAssessmentDeleteView.as_view(),
        name='individual-assessment-delete'
    ),
    path(
        'individual-assessment-update/<int:pk>/',
        views.IndividualAssessmentUpdateView.as_view(),
        name='individual-assessment-update'
    ),
    path(
        'help/',
        views.AssessmentHelpView.as_view(),
        name='assessment-help'
    ),
    # url for Institution Assessment type views
    path(
        'create-institution-assessment/',
        views.InstitutionAssessmentCreateView.as_view(),
        name='create-institution-assessment'
    ),
    path(
        'institution-assessment-list/',
        views.InstitutionAssessmentListView.as_view(),
        name='institution-assessment-list'
    ),
    path(
        'institution-assessment-detail/<int:pk>/',
        views.InstitutionAssessmentDetailView.as_view(),
        name='institution-assessment-detail'
    ),
    path(
        'institution-assessment-update/<int:pk>/',
        views.InstitutionAssessmentUpdateView.as_view(),
        name='institution-assessment-update'
    ),
    path(
        'institution-assessment-delete/<int:pk>/',
        views.InstitutionAssessmentDeleteView.as_view(),
        name='institution-assessment-delete'
    ),
    # paths for Sample Assessments
    path(
        'sample-assessment-list/',
        views.SampleAssessmentListView.as_view(),
        name='sample-assessment-list'
    ),
]
