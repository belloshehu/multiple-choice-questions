from . import views
from django.urls import path


app_name = 'multiple_choices'
urlpatterns = [
    path(
        'instruction/<int:pk>/',
        views.AssessmentInstructionView.as_view(),
        name='instruction'
    ),
    path('assessment/', views.assessment, name='assessment'),
    path('result/', views.process_result, name='result'),
    path('create-test/', views.create_cbt, name='create_test'),
    path('sample/', views.sample, name='sample'),
    path(
        'assessment-taking/<int:pk>/',
        views.AssessmentTakingView.as_view(),
        name='assessment-taking'
    ),
    path(
        'assessment-window/',
        views.AssessmentWindowView.as_view(),
        name='assessment-window'
    ),
    path(
        'get-associated-choices/',
        views.QuestionAssociatedChoicesView.as_view(),
        name='get-associated-choices'
    )
]