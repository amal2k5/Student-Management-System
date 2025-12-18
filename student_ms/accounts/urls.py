from django.urls import path
from . import views
from accounts.views import student_full_register
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path("register-full/", student_full_register, name="student_full_register"),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"
    ), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ), name='password_reset_complete'),
    
    path("student/<int:pk>/", views.student_detail, name="student_detail"),



]
