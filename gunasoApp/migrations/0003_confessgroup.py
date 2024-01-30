# Generated by Django 5.0.1 on 2024-01-30 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gunasoApp', '0002_remove_userpost_category_userpost_visiteduser_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfessGroup',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('Groupname', models.CharField(max_length=30)),
                ('creationDate', models.DateField(auto_now_add=True)),
                ('tagline', models.CharField(blank=True, max_length=212)),
                ('slug', models.CharField(default='slugthis', max_length=130)),
                ('image', models.ImageField(blank=True, default='upload-image', upload_to='gunasoApp/images/groupImages')),
                ('introduction', models.TextField(blank=True)),
            ],
        ),
    ]
