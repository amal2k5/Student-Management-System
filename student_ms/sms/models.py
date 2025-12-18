from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100)
    year_of_admission = models.PositiveIntegerField()
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='students/', null=True, blank=True)

    def __str__(self):
        return self.name
