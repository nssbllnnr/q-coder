from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from django.views import View 
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from ..models import *
from ..forms import *
from users.models import *
from users.forms import *
from ..decorators import *
import random
import string

@method_decorator([login_required], name='dispatch')
class CourseView(View):
    form_class = CourseForm
    initial = {'key': 'value'}
    template_name = 'qmain/courses.html'

    def get(self, request, id = 0):
        if id != 0:
            course = get_object_or_404(Course, pk=id)
            form = self.form_class(instance=course)  
        else:
            form = self.form_class(initial=self.initial)
        context = {
            'courses' : self.get_courses(request),
            'title' : 'Courses',
            'form': form,
            'user_is_teacher': self.is_member(request.user),
            'user_is_student': self.is_student(request.user)
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            course = form.save()
            course.lector = Teacher.objects.get(user = request.user)
            course.entry_code = self.random_entry_code()
            course.save()
        context = {
            'courses' : self.get_courses(request),
            'title' : 'Courses',
            'form': form,
            'user_is_teacher': self.is_member(request.user),
            'user_is_student': self.is_student(request.user)
        }
        return render(request, self.template_name, context=context)

    def get_courses(self, request):
        try:
            if self.is_member(request.user):
                return Course.objects.filter(lector=Teacher.objects.get(user = request.user))
            else:
                return Course.objects.filter(students__in=[Student.objects.get(user=request.user)])
        except Course.DoesNotExist:
            return None

    def is_member(self, user):
        return user.groups.filter(name='Teacher').exists()
        
    def is_student(self, user):
        return user.groups.filter(name='Student').exists()
        
    #Create random entry code for course.
    def random_entry_code(self):
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        rnd= ''.join(random.choice(letters) for i in range(8))
        return rnd

@method_decorator([login_required], name='dispatch')
class CourseUpdateView(View):
    template_name = 'qmain/course_update_form.html'
    def get(self, request, id = 0):
        course = get_object_or_404(Course, pk=id)
        form = CourseForm(instance=course)
        context = {
            'form': form,
            'id': id,
            'title': 'Courses'
        }
        return render(request, self.template_name, context=context)

    def post(self, request, id = 0):
        course = get_object_or_404(Course, pk=id)
        form = CourseForm(request.POST,instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses')
        else:
            context = {
                'form':form,
                'id':id,
                'title': 'Courses'
            }
            return render(request, self.template_name, context=context) 


    def get_courses(self, request):
        try:
            if self.is_member(request.user):
                return Course.objects.filter(lector=Teacher.objects.get(user = request.user))
            else:
                return Course.objects.filter(students__in=[Student.objects.get(user=request.user)])
        except Course.DoesNotExist:
            return None

@method_decorator([login_required], name='dispatch')
class CourseDeleteView(View):
    def get(self, request, id = 0):
        course = get_object_or_404(Course, pk=id)
        course.delete()
        return redirect('courses')

@login_required
@allowed_users(allowed_roles=['Student'])
def joinCourse(request):
    if request.method == 'POST':
        student=Student.objects.get(user=request.user)
        course = Course.objects.get(entry_code=request.POST['entry_code'])
        course.students.add(student)
        
    return redirect('courses')
    