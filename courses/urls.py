from django.urls import path
from courses.views import (CourseCreateView, CourseDeleteView, CourseUpdateView,
                           ManageCourseListView, CourseSectionUpdateView, UnitCreateUpdateView,
                           UnitDeleteView, SectionUnitListView,
                           SectionOrderView, UnitOrderView,
                           CourseListView, CourseDetailView)


urlpatterns = [
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('<pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('mine/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('<pk>/section/', CourseSectionUpdateView.as_view(), name='course_section_update'),
    path('section/<int:section_id>/', SectionUnitListView.as_view(), name='section_unit_list'),
    path('section/<int:section_id>/unit/<model_name>/create/', UnitCreateUpdateView.as_view(),
         name='section_unit_create'),
    path('section/<int:section_id>/unit/<model_name>/<id>/', UnitCreateUpdateView.as_view(),
         name='section_unit_update'),
    path('section/<int:unit_id>/delete/', UnitDeleteView.as_view(), name='section_unit_delete'),

    path('unit/order/', UnitOrderView.as_view(), name='unit_order'),
    path('section/order/', SectionOrderView.as_view(), name='section_order'),

    path('subject/<slug:subject>/', CourseListView.as_view(), name='course_list_subject'),
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
]
