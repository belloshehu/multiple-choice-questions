from django.urls import path
from . import views
from multiple_choices.views import sample
from django.contrib.auth import urls

app_name = 'cbt'
urlpatterns = [
    path('', views.home, name='home'),
    path(
        'cbt-list/',
        views.IndividualAssessmentListView.as_view(),
        name='cbt_list'
    ),
    path('cbt-type', views.cbt_type, name='cbt_type'),
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
    # Individual cbt url
    path(
        'create-individual-assessment/',
        views.IndividualAssessmentCreateView.as_view(),
        name='create-individual-assessment'
    ),
    path(
        'individual-assessment-detail/<int:pk>/',
        views.IndividualAssessmentDetailView.as_view(),
        name='individual-assessment-detail'
    ),
    path(
        'create-organisation-assessment/',
        views.OrganisationAssessmentCreateView.as_view(),
        name='create-organisation-assessment'
    ),
    path(
        'help/',
        views.AssessmentHelpView.as_view(),
        name='assessment-help'
    )
]
