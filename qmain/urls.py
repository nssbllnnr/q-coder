from django.urls import path, re_path, include
from .views import main, courses, assignments

urlpatterns = [
    path('', main.MainView.as_view(), name='main'),
    path('courses', courses.CourseView.as_view(), name='courses'),
    path('joinCourse', courses.joinCourse, name='joinCourse'),
    path('course/<int:id>/update', courses.CourseUpdateView.as_view(), name='updateCourse'),
    path('course/<int:id>/delete', courses.CourseDeleteView.as_view(), name='deleteCourse'),
    path('course/<int:id>/students', assignments.students, name='students'),
    path('course/<int:id>/tasks', assignments.course, name='course'),
    path('course/<int:course_id>/tasks/<int:task_id>', assignments.exam_evaluation, name='exams'),
    path('course/<int:course_id>/tasks/<int:task_id>/bubble_sheet', assignments.bubble_sheet, name='bubble_sheet'),
    path('course/<int:course_id>/tasks/<int:task_id>/list',assignments.task, name='task'),
]
