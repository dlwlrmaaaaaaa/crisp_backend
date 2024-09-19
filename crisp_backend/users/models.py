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
        return self.user.email

# Define DepartmentAdmin model
class DepartmentAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department_admin_profile')
    contact_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    address = models.TextField(),

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

# Define Report model
class Report(models.Model):
    report_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Citizen, on_delete=models.CASCADE)  # Use Citizen model as an example
    image_path = models.CharField(max_length=100)
    type_of_report = models.CharField(max_length=100)
    report_description = models.CharField(max_length=255)
    report_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_of_report