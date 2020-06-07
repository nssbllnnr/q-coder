from django.urls import path, re_path, include
from .views import main, courses, assignments, quizzes


urlpatterns = [
    path('', main.MainView.as_view(), name='main'),
    path('courses', courses.CourseView.as_view(), name='courses'),
    path('joinCourse', courses.joinCourse, name='joinCourse'),
    path('course/<int:id>/update', courses.CourseUpdateView.as_view(), name='updateCourse'),
    path('course/<int:id>/delete', courses.CourseDeleteView.as_view(), name='deleteCourse'),
    path('course/<int:id>/students', assignments.students, name='students'),
    path('course/<int:id>/tasks', assignments.course, name='course'),
    path('course/<int:course_id>/tasks/<int:task_id>', assignments.exam_evaluation, name='exams'),
    path('course/<int:course_id>/tasks/<int:task_id>/list',assignments.task, name='task'),
    path('course/<int:course_id>/quizzes', quizzes.home, name='quizzes'),
    path('course/<int:course_id>/quizzes/create/', quizzes.create, name= 'quizzes-create'),
    path('course/<int:course_id>/quizzes/vote/<poll_id>/', quizzes.vote, name= 'quizzes-vote'),
    path('course/<int:course_id>/quizzes/results/<poll_id>/', quizzes.results, name= 'quizzes-results'),
]
