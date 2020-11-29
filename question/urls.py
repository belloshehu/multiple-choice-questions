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
    )
]