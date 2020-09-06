from . import views
from django.urls import path


app_name = 'multiple_choices'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('assessment/', views.assessment, name='assessment'),
    path('result/', views.process_result, name='result'),
    path('logout/', views.user_logout, name='logout'),
    path('create-test/', views.create_cbt, name='create_test')
]