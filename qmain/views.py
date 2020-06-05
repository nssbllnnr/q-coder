from django.shortcuts import render, redirect
from .models import Course, Student, Task, Assignments
from django.contrib import messages
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.models import Teacher, Student
from .forms import CourseForm, TaskForm
from django.views import View 
from .decorators import allowed_users,teacher_only,unlogined_user
import random
import string
import os
import io
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import cv2
from PyPDF2 import PdfFileWriter, PdfFileReader
from pytesseract import pytesseract
from difflib import SequenceMatcher
from PIL import Image
pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'


"""
    Main page show landing page with registration form.
"""
def main(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            if group.name == 'Teacher':
                    Teacher.objects.create(user=user)
            elif group.name == 'Student':
                    Student.objects.create(user=user)
            user.groups.add(group)
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'qmain/landing.html', {'form': form})

#@method_decorator([login_required], name='dispatch')
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

    # def post(self, request, id = 0):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         course = form.save()
    #         course.lector = Teacher.objects.get(user = request.user)
    #         course.entry_code = random_entry_code()
    #         course.save()
    #     form = self.form_class(initial=self.initial)
    #     context = self.get_context_data(request, form, **kwargs)
    #     return render(request, self.template_name, context=context)

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


"""
    Page of courses list. Have course creating form.
"""
@login_required
def courses(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            course.lector = Teacher.objects.get(user = request.user)
            course.entry_code = random_entry_code()
            course.save()
    try:
        if is_member(request.user):
            courses = Course.objects.filter(lector=Teacher.objects.get(user = request.user))
        else:
            courses = Course.objects.filter(students__in=[Student.objects.get(user=request.user)])
    except Course.DoesNotExist:
        courses = None
        
    context = {
        'courses' : courses,
        'title' : 'Courses',
        'form': form,
        'user_is_teacher': is_member(request.user),
        'user_is_student': is_student(request.user)
    }
    return render(request, 'qmain/courses.html', context)

"""
    Give permission for creating a courses to the Teacher.
"""
def is_member(user):
    return user.groups.filter(name='Teacher').exists()
def is_student(user):
    return user.groups.filter(name='Student').exists()
"""
    Create random entry code for course.
"""
def random_entry_code():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    rnd= ''.join(random.choice(letters) for i in range(8))
    return rnd

#code which We didn't use)))
@login_required
def assignments(request):
    return render(request, 'qmain/assignments.html', {'title':'Assignments'})

"""
    Page with all student in the course.
"""
@login_required
def students(request, id):
    students = Course.objects.get(id=id).students.all()
    return render(request, 'qmain/students.html', {'title':'Students', 'students':students, 'course_id':id})

"""
    Page with all tasks in the course.
    In this page teacher can create a new task.
"""
@login_required
def course(request, id):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.course_id = id
            task.save()
        else:
            print('NO')
    form = TaskForm()
    tasks = Task.objects.filter(course_id=Course.objects.get(id=id))
    return render(request, 'qmain/course.html', {'title':'Tasks', 'tasks':tasks, 'course_id':id, 'form':form})

"""
    Ulzhan's code for checking exams.
"""
@login_required
def check_exam(request, course_id, task_id):
    if request.method == 'POST':
        path = 'media/diploma.pdf'
        fname = os.path.splitext(os.path.basename(path))[0]
        pdf = PdfFileReader(path)
        #split pdf file to multiple pds
        for page in range(pdf.getNumPages()):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            output_filename = 'media/diploma/{}_page_{}.pdf'.format(
                fname, page+1)
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
            #print('Created: {}'.format(output_filename))
            
        #convert pdf to png, because tesseracts workd only with png file 
        for page in range(pdf.getNumPages()):
            images = convert_from_path('media/diploma/{}_page_{}.pdf'.format(
                fname, page+1))
            for image in images:
                image.save('media/diploma/{}_page_{}.png'.format(fname, page+1),'PNG')
                image_name2 = 'media/diploma/{}_page_{}.png'.format(fname, page+1)
                #crop name or id
                img = Image.open(image_name2)
                student_id = img.crop((430, 0, 920, 276))
                student_id.save('media/diploma/student_{}.png'.format(page+1))
                img_cv = cv2.imread('media/diploma/student_{}.png'.format(page+1))
                student_id_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                student_id_text =pytesseract.image_to_string(student_id_rgb)
                if User.objects.filter(groups__name='Student').filter(last_name=student_id_text).exists():
                    #tesseract converts handwriting to txx file 
                    img_cv = cv2.imread(image_name2)
                    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                    new =pytesseract.image_to_string(img_rgb)
                    true_answers = open('media/RightAnswers.txt').read()
                    m = SequenceMatcher(None, new, true_answers) #insert mark
                    mark = m.ratio()*1388 #insert markz
                    Assignments.objects.create(grade=mark, task=Task.objects.get(id=task_id), student=Student.objects.get(user= User.objects.filter(groups__name='Student').filter(last_name=student_id_text).first()))
    assignments = Assignments.objects.filter(task_id=task_id)
    return  render(request, 'qmain/check_exam.html', {'title':'Exam check', 'course_id':course_id, 'task_id':task_id, 'assignments':assignments})

"""
    List of the task assignments.
"""
@login_required
def task(request, course_id, task_id):
    assignments = Assignments.objects.filter(task_id=task_id)
    return  render(request, 'qmain/task.html', {'title':'Task assignmets', 'course_id':course_id, 'assignments':assignments})
