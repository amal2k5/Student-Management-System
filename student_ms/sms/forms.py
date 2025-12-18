from django import forms
from accounts.models import User
from .models import Student


class AdminAddStudentForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    name = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    year_of_admission = forms.IntegerField()
    roll_number = forms.CharField(max_length=50)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
)

    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "name",
            "roll_number",
            "department",
            "year_of_admission",
            "date_of_birth",
            "profile_pic",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "roll_number": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "year_of_admission": forms.NumberInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "profile_pic": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control'})


class AdminUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        } 
        
class AdminPasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned = super().clean()
        if cleaned["password1"] != cleaned["password2"]:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned
                



