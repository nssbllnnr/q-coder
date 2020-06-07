from django.urls import path, re_path, include
from .views import main, courses, assignments

urlpatterns = [
<<<<<<< HEAD
    path('', views.main, name='main'),
    path('courses', views.courses, name='courses'),
    path('assignments', views.assignments, name='assignments'),
    path('course/<int:id>/students', views.students, name='students'),
    path('course/<int:id>/tasks', views.course, name='course'),
    path('course/<int:course_id>/tasks/<int:task_id>', views.check_exam, name='exams'),
    path('course/<int:course_id>/tasks/<int:task_id>/list',views.task, name='task'),
    path('joinCourse', views.joinCourse, name='joinCourse'),
    
]

=======
    path('', main.MainView.as_view(), name='main'),
    path('courses', courses.CourseView.as_view(), name='courses'),
    path('joinCourse', courses.joinCourse, name='joinCourse'),
    path('course/<int:id>/update', courses.CourseUpdateView.as_view(), name='updateCourse'),
    path('course/<int:id>/delete', courses.CourseDeleteView.as_view(), name='deleteCourse'),
    path('course/<int:id>/students', assignments.students, name='students'),
    path('course/<int:id>/tasks', assignments.course, name='course'),
    path('course/<int:course_id>/tasks/<int:task_id>', assignments.exam_evaluation, name='exams'),
    path('course/<int:course_id>/tasks/<int:task_id>/list',assignments.task, name='task'),
]
>>>>>>> af1227b022a797538ff1780c0779fdbc03ce2d5a
