# Generated by Django 3.0.5 on 2020-06-10 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qmain', '0017_auto_20200611_0218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmenthistory',
            old_name='name',
            new_name='student_fio',
        ),
        migrations.RemoveField(
            model_name='assignmenthistory',
            name='surname',
        ),
    ]