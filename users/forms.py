from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateTimeInput, DateTimeField
from .models import Teacher, Student


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username','email','group','password1','password2']


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude= ['user']

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude= ['user']