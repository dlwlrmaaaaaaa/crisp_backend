# Generated by Django 4.2.16 on 2024-09-20 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='upvote',
            field=models.IntegerField(default=0),
        ),
    ]
