from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Citizen, DepartmentAdmin, SuperAdmin, Worker

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.groups.filter(name='Citizen').exists():
            Citizen.objects.create(user=instance)
        elif instance.groups.filter(name='DepartmentAdmin').exists():
            DepartmentAdmin.objects.create(user=instance)
        elif instance.groups.filter(name='SuperAdmin').exists():
            SuperAdmin.objects.create(user=instance)
        elif instance.groups.filter(name='Worker').exists():
            Worker.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'citizen_profile'):
        instance.citizen_profile.save()
    if hasattr(instance, 'department_admin_profile'):
        instance.department_admin_profile.save()
    if hasattr(instance, 'super_admin_profile'):
        instance.super_admin_profile.save()
    if hasattr(instance, 'worker_profile'):
        instance.worker_profile.save()
