from .models import User
from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm



   
        

class FullStudentRegistrationForm(UserCreationForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    department = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    year_of_admission = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )

    profile_pic = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
    


class AdminUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        
        
        
        
        
        
