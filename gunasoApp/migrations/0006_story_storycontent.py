# Generated by Django 5.0.1 on 2024-01-05 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gunasoApp', '0005_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='storyContent',
            field=models.TextField(blank=True),
        ),
    ]