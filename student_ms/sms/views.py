from accounts.forms import AdminUserUpdateForm
from .forms import AdminAddStudentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError
from .models import Student
from .forms import StudentForm
from accounts.forms import FullStudentRegistrationForm
from accounts.models import User



admin_required = user_passes_test(
    lambda u : u.is_authenticated and u.role == "admin",
    login_url='/accounts/login/'
)


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    if request.user.role == "admin":
        return redirect("sms:admin_dashboard")
    return redirect("sms:student_dashboard")



@admin_required
def admin_dashboard(request):
    search_query = request.GET.get("q", "")

    students = Student.objects.filter(
        Q(name__icontains=search_query) |
        Q(roll_number__icontains=search_query) |
        Q(user__email__icontains=search_query) |
        Q(department__icontains=search_query)
    ).order_by("name")

    paginator = Paginator(students, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "sms/admin_portal/admin_dashboard.html", {
        "students": students,
        "page_obj": page_obj,
        "search_query": search_query,
    })


@admin_required
def student_list(request):
    search_query = request.GET.get("q", "")

    students = Student.objects.filter(
        Q(name__icontains=search_query) |
        Q(roll_number__icontains=search_query) |
        Q(user__email__icontains=search_query) |
        Q(department__icontains=search_query)
    ).order_by("name")

    paginator = Paginator(students, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "sms/admin_portal/student_list.html", {
        "page_obj": page_obj,
        "search_query": search_query
    })


@admin_required
def student_create(request):

    if request.method == "POST":
        form = AdminAddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            if form.cleaned_data["password1"] != form.cleaned_data["password2"]:
                messages.error(request, "Passwords do not match.")
                return render(request, "sms/admin_portal/student_create.html", {"form": form})

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"]
            )
            user.role = "student"
            user.save()

            Student.objects.create(
                user=user,
                name=form.cleaned_data["name"],
                department=form.cleaned_data["department"],
                year_of_admission=form.cleaned_data["year_of_admission"],
                roll_number=form.cleaned_data["roll_number"],
                date_of_birth=form.cleaned_data.get("date_of_birth"),
                profile_pic=form.cleaned_data.get("profile_pic"),
            )

            messages.success(request, "Student created successfully.")
            return redirect("sms:admin_dashboard")

        messages.error(request, "Please correct the errors below.")

    else:
        form = AdminAddStudentForm()

    return render(request, "sms/admin_portal/student_create.html", {"form": form})

@admin_required
def student_edit(request, pk):
    student = Student.objects.get(id=pk)
    user = student.user

    if request.method == "POST":
        user_form = AdminUserUpdateForm(request.POST, instance=user)
        student_form = StudentForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            messages.success(request, "Student details updated successfully.")
            return redirect("sms:student_list")

     
        print("User form errors:", user_form.errors)
        print("Student form errors:", student_form.errors)

        messages.error(request, "Please correct the errors below.")

    else:
        user_form = AdminUserUpdateForm(instance=user)
        student_form = StudentForm(instance=student)

    return render(request, "sms/admin_portal/student_edit_profile.html", {
        "user_form": user_form,
        "student_form": student_form,
        "student": student,
    })


@admin_required
def student_delete(request, pk):
    student = Student.objects.get(id=pk)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("sms:admin_dashboard")




@login_required
def student_dashboard(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        messages.info(request, "Please complete your student registration.")
        return redirect("sms:register_student")

    return render(request, "sms/student_portal/student_dashboard.html", {"student": student})


@login_required
def student_edit_profile(request):
    student = Student.objects.get(user=request.user)
    user = request.user

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()

            new_email = request.POST.get("email")
            if new_email and new_email != user.email:
                user.email = new_email
                user.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("sms:student_dashboard")

        messages.error(request, "Please correct the errors below.")

    else:
        form = StudentForm(instance=student)

    return render(request, "sms/student_portal/edit_profile.html", {
        "form": form,
        "student": student,
        "user": user,
    })




def student_full_register(request):
    if request.method == "POST":
        form = FullStudentRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"]
            )
            user.role = "student"
            user.save()

            try:
                Student.objects.create(
                    user=user,
                    name=form.cleaned_data["name"],
                    department=form.cleaned_data["department"],
                    year_of_admission=form.cleaned_data["year_of_admission"],
                    profile_pic=form.cleaned_data.get("profile_pic"),
                )

                messages.success(request, "Account created successfully. Welcome!")
                login(request, user)
                return redirect("sms:student_dashboard")

            except IntegrityError:
                user.delete()
                messages.error(request, "Student with this email already exists.")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = FullStudentRegistrationForm()

    return render(request, "registration/student_register_full.html", {"form": form})



def student_detail(request, pk):
    student = get_object_or_404(Student, id=pk)
    return render(request, "sms/student_detail.html", {"student": student})
