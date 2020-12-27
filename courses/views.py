from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

import logging
from courses.models import Course
# Create your views here.
logger = logging.getLogger('zubair')


class AuthorMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class AuthorEditMixin(object):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AuthorCourseMixin(AuthorMixin, LoginRequiredMixin,
                        PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class ManageCourseListView(AuthorCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class AuthorCourseEditMixin(AuthorCourseMixin, AuthorEditMixin):
    template_name = 'courses/manage/course/form.html'


class CourseCreateView(AuthorCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(AuthorCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(AuthorCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class MyView(View):

    def get(self, request, *args, **kwargs):
        logger.info("Welcome to Logging Mr.Zubair")
        return HttpResponse("Welcome to Views 101")

