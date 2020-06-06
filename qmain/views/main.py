from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from django.views import View 
from ..models import *
from ..forms import *
from users.models import *
from users.forms import *
from ..decorators import *

class MainView(View):
    form_class = UserRegisterForm
    initial = {'key': 'value'}
    template_name = 'qmain/courses.html'
    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, 'qmain/landing.html', {'form': form})

    def post(self, request):
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
        return render(request, 'qmain/landing.html', {'form': form})

