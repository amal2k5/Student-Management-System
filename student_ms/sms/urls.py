from django.urls import path
from . import views

app_name = "sms"

urlpatterns = [


    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),

  
    path("students/", views.student_list, name="student_list"),
    path("students/create/", views.student_create, name="student_create"),
    path("students/<int:pk>/edit/", views.student_edit, name="student_edit"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),


    path("profile/edit/", views.student_edit_profile, name="student_edit_profile"),
    path("student/<int:pk>/", views.student_detail, name="student_detail"),
]
