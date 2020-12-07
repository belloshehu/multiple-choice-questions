from django.urls import path
from . import views

app_name = 'choice'

urlpatterns = (
    path(
        'create/<int:pk>/',
        views.IndividualChoiceCreateView.as_view(),
        name='individual-create'
    ),
    path(
        'update/<int:pk>/',
        views.IndividualChoiceUpdateView.as_view(),
        name='individual-update'
    ),
    path(
        'delete/<int:pk>/',
        views.IndividualChoiceDeleteView.as_view(),
        name='individual-delete'
    )
)