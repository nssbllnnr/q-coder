from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from django.views import View 
from django.db.models import Value as V
from django.db.models.functions import Concat 
from ..models import *
from ..forms import *
from users.models import *
from users.forms import *
from ..decorators import *
from .exam_evaluate import exam_evaluate_map, get_mark, mark
import random
import string
import ast

@method_decorator([login_required], name='dispatch')
class AssignmentsView(View):
    form_class = CourseForm
    initial = {'key': 'value'}
    template_name = 'qmain/courses.html'


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
def exam_evaluation(request, course_id, task_id):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid:
            task_files = form.save(commit=False)
            task_files.task_file_id = task_id
            task_files.save()
            path = 'media/{}'.format(task_files.exam_file.name)
            path_answers = 'media/{}'.format(task_files.answers_file.name)
            data = exam_evaluate_map(path)
            AssignmentHistory.objects.filter(task_id=task_id).delete()
            Assignments.objects.filter(task_id=task_id).delete()
            for key in data:
                mark = get_mark(data[key], path_answers)
                AssignmentHistory.objects.create(grade=mark, 
                                                 task=Task.objects.get(id=task_id), 
                                                 student_fio = key)
                if User.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(full_name__icontains=key).exists():
                    _user = User.objects.filter(groups__name='Student').\
                                            annotate(full_name=Concat('first_name', V(' '), 'last_name')).\
                                            filter(full_name__icontains=key).first()
                    _student = Student.objects.get(user=_user)
                    Assignments.objects.create( grade=mark, 
                                                task=Task.objects.get(id=task_id), 
                                                student=_student)
    assignments = Assignments.objects.filter(task_id=task_id)
    assignments_history = AssignmentHistory.objects.filter(task_id=task_id)
    TaskLinks.objects.filter()
    form = DocumentForm()
    return  render(request, 
                   'qmain/check_exam.html', 
                   {
                        'title':'Exam check', 
                        'course_id':course_id, 
                        'task_id':task_id, 
                        'assignments' : assignments, 
                        'assignments_history' :assignments_history,
                        'form':form
                   })


@login_required
def bubble_sheet(request, course_id, task_id):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid:
            task_files = form.save(commit=False)
            task_files.task_file_id = task_id
            task_files.save()
            path = 'media/{}'.format(task_files.exam_file.name)
            path_answers = 'media/{}'.format(task_files.answers_file.name)
            #{0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
            file = open(path_answers,'r')
            answer = ast.literal_eval(file.read())
            print(answer)
            score = mark(path, answer)
            Assignments.objects.filter(task_id=task_id).delete()
            Assignments.objects.create( grade=score, 
                                        task=Task.objects.get(id=task_id))
    assignments = Assignments.objects.filter(task_id=task_id)
    return  render(request, 
                   'qmain/bubble_sheet.html', 
                   {
                        'title':'Exam check', 
                        'course_id':course_id, 
                        'task_id':task_id, 
                        'assignments' : assignments, 
                        'form':form
                   })


"""
    List of the task assignments.
"""
@login_required
def task(request, course_id, task_id):
    assignments = Assignments.objects.filter(task_id=task_id)
    return  render(request, 'qmain/task.html', {'title':'Task assignmets', 'course_id':course_id, 'assignments':assignments})



