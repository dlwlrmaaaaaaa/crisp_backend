# Generated by Django 5.1 on 2024-09-22 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_report_location_report_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmentadmin',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
