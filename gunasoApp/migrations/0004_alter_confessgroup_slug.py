# Generated by Django 5.0.1 on 2024-01-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gunasoApp', '0003_confessgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confessgroup',
            name='slug',
            field=models.CharField(blank=True, max_length=130, unique=True),
        ),
    ]
