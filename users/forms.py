from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, Textarea, PasswordInput
from django.contrib.auth.models import User, Group
from django import forms
<<<<<<< HEAD
from django.forms import ModelForm, TextInput, Textarea, DateTimeInput, DateTimeField
from .models import Teacher, Student
=======
from crispy_forms.helper import FormHelper
from django import forms

class MyForm(forms.Form):
    [...]

>>>>>>> af1227b022a797538ff1780c0779fdbc03ce2d5a


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        
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