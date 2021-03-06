from django.forms import *
from .models import *
from .models import Poll
from django.forms import ModelForm


# Create the form class.
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description','year', 'term']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control validate', 'placeholder':'Title'}),
            'code': TextInput(attrs={'class':'form-control validate',  'placeholder':'Code'}),
            'description': Textarea(attrs={'class':'form-control validate',  'placeholder':'Description'}),
            'year': TextInput(attrs={'class': 'form-control validate',  'placeholder':'Year'}),
            'term': Select(attrs={'class': 'form-control validate',  'placeholder':'Term'}),
        }

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control validate', 'id':'orangeForm-name','placeholder':'Title'}),
            'description': Textarea(attrs={'class':'md-textarea form-control','placeholder':'Description','rows':'3'}),
            'deadline' : DateTimeInput(attrs={'type':'date'}, format="%d-%m-%Y %H:%M:%S")
        }



class DocumentForm(ModelForm):
    class Meta:
        model = TaskLinks
        fields = ['exam_file', 'answers_file']




class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three']
