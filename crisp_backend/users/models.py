
from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Define Citizen model
class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen_profile')
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.user.username

class DepartmentAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department_admin_profile')
    contact_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)  # Allow null values


    def __str__(self):
        return self.user.email

class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='super_admin_profile')
    contact_number = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.user.email

class Workers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='workers_profile')
    contact_number = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.user.email
    

class Report(models.Model):
    report_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Citizen, on_delete=models.CASCADE)  # Use Citizen model as an example
    image_path = models.CharField(max_length=255)
    type_of_report = models.CharField(max_length=100)
    report_description = models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    upvote = models.IntegerField(default=0)
    report_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return self.type_of_report

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Feedback(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)