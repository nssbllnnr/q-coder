# Generated by Django 3.0.5 on 2020-06-06 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_student_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='teacher',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]