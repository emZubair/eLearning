from django.urls import path

from .views import (StudentRegistrationView, StudentEnrollCourseView,
                    StudentCourseDetailView, StudentCourseListView)

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='student_registration'),
    path('course-enroll/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/', StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<pk>/', StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/<pk>/<section_id>/', StudentCourseDetailView.as_view(), name='student_course_detail_section')

]

