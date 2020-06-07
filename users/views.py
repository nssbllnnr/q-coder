from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.models import Student, Teacher
from .forms import TeacherForm, StudentForm
from django.views import View 

"""
    Registration form of users, when we also create 
    Student or Teacher models. After registration redirect to login page.
"""
def register(request):
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
            messages.success(request, f'Account created for {username} {group}!')
            return redirect('login_url')
    elif request.method == 'GET':
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})
    else:
        return render(request, 'users/register.html', {'form': form})

"""
    User profile page.
"""
@login_required
def profile(request):
    teacher=Teacher.objects.get(user=request.user)
    form=TeacherForm()
    if request.method=='POST':
        if is_member(teacher):
            form=TeacherForm(request.POST,request.FILES,instance=teacher)
            if form.is_valid:
                form.save()
    
    context={'form':form}
    return render(request, 'users/profile.html', context)

def is_member(user):
    return user.groups.filter(name='Teacher').exists()
def is_student(user):
    return user.groups.filter(name='Student').exists()