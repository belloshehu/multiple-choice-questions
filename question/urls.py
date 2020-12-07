from django.urls import path
from question import views

app_name = 'question'
urlpatterns = [
    path(
        'individual-create/<int:pk>/',
        views.IndividualQuestionCreateView.as_view(),
        name='individual-create'
    ),
    path(
        'individual-from-passage-create/<int:pk>/',
        views.IndividualQuestionFromPassageCreateView.as_view(),
        name='individual-question-from-passage-create'
    ),
    path(
        'Individual-details/<int:pk>/',
        views.IndividualQuestionDetailView.as_view(),
        name='individual-detail'
    ),

    path(
        'individual-list/',
        views.IndividualQuestionListView.as_view(),
        name='individual-list'
    ),
    path(
        'update/<int:pk>/',
        views.IndividualQuestionUpdateView.as_view(),
        name='update'
    ),
    path(
        'delete/<int:pk>/',
        views.IndividualQuestionDeleteView.as_view(),
        name='delete'
    ),
    path(
        'individual-question-choices/<int:pk>/',
        views.IndividualQuestionChoiceView.as_view(),
        name='individual-question-choices'
    ),
    path(
        'individual-passage-create/<int:pk>/',
        views.IndividualQuestionPassageCreateView.as_view(),
        name='individual-passage-create'
    ),
    #path(
    #    'institution-question-choices/<int:pk>/',
    #    views.InstitutionQuestionChoiceView.as_view(),
    #    name='institution-question-choices'
    #)
]