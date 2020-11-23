from django.urls import path
from . import views
from multiple_choices.views import sample
from django.contrib.auth import urls

app_name = 'cbt'
urlpatterns = [
    path('create_cbt/', views.create_cbt, name='create_cbt' ),
    path('', views.home, name='home'),
    path('cbt-list/', views.cbt_list, name='cbt_list'),
    path('cbt-type', views.cbt_type, name='cbt_type'),
    path(
        'create-institution-cbt/',
        views.create_institution_cbt,
        name='create_institution'
    ),
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

]
