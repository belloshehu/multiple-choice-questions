from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('reset-password/',
        views.PasswordResetView.as_view(), name='reset_password'
    ),
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/password/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/password/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
        ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='account/password/password_reset_complete.html'
            ),
        name='password_reset_complete',
        ),
    path(
        'dashboard/',
        views.DashboardView.as_view(),
        name='dashboard'
    ),
    path(
        'update/<int:pk>/',
        views.UserAccountUpdateView.as_view(),
        name='account-update'
    )
]