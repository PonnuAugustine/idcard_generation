# Generated by Django 5.1.1 on 2024-10-23 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_student_course_name_student_department'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student',
        ),
    ]
