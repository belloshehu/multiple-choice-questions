from django.urls import path
from . import views
from multiple_choices.views import sample
from django.contrib.auth import urls

app_name = 'cbt'
urlpatterns = [
    path('create_cbt/', views.create_cbt, name='create_cbt' ),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('cbt-list/', views.cbt_list, name='cbt_list'),
    path('cbt-type', views.cbt_type, name='cbt_type'),
    path('create-institution-cbt/', views.create_institution_cbt, name='create_institution'),
    path('create-institution/', views.create_institution, name='create_institution'),
    path('logout', views.user_logout, name='logout'),
    path('sample/', sample, name='sample'),
    path('password_reset/', views.password_reset, name='password_reset'),
]

