from sms.models import Student 
from django.contrib.auth import login
from accounts.forms import FullStudentRegistrationForm
from django.shortcuts import render, redirect,get_object_or_404


def student_full_register(request):
    if request.method == "POST":
        form = FullStudentRegistrationForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.role = "student"
            user.email = form.cleaned_data["email"]  
            user.save()

            Student.objects.create(
                user=user,
                name=form.cleaned_data["name"],
                department=form.cleaned_data["department"],
                year_of_admission=form.cleaned_data["year_of_admission"],
                profile_pic=form.cleaned_data.get("profile_pic"),
            )

            login(request, user)

            return redirect("sms:student_dashboard")
    else:
        form = FullStudentRegistrationForm()

    return render(request, "registration/student_register_full.html", {"form": form})


def student_detail(request, pk):
    student = get_object_or_404(Student, id=pk)
    return render(request, "student_detail.html", {"student": student})



