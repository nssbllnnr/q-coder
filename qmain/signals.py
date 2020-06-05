from django.contrib.auth.models import User
from users.models import Student, Teacher
from django.db.models.signals import post_save,pre_save, post_delete
from django.dispatch import receiver
from .models import Course, Task

@receiver(post_save, sender=Teacher)

def course_update(sender,instance,**kwargs):
    instance.course.save()
    print("Course was updated")
post_save.connect(course_update,sender=Teacher)