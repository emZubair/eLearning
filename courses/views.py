from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.apps import apps
from django.views.generic.list import ListView
from django.forms.models import modelform_factory
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

import logging
from courses.forms import ModuleFormSet
from courses.models import Course, Section, Unit
# Create your views here.
logger = logging.getLogger('zubair')
MODEL_CHOICES = 'text video image file'


# Subject -> Courses -> Module -> Content
# Subject -> Courses -> Section -> Units
# Units -> ContentBase -> Text, video, image, audio


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


class CourseSectionUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/section/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk,
                                        author=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({
            'course': self.course, 'formset': formset
        })

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({
            'course': self.course, 'formset': formset
        })


class UnitCreateUpdateView(TemplateResponseMixin, View):
    section = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    @staticmethod
    def get_model(model_name):
        if model_name in MODEL_CHOICES:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=[
            'author', 'order', 'created', 'updated'
        ])
        return Form(*args, **kwargs)

    def dispatch(self, request, section_id, model_name, id=None):
        self.section = get_object_or_404(Section, id=section_id,
                                         course__author=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, author=request.user)
        return super().dispatch(request, section_id, model_name, id)

    def get(self, request, section_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({
            'form': form, 'object': self.obj
        })

    def post(self, request, section_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj,
                             data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            if not id:
                Unit.objects.create(section=self.section, item=obj)
            return redirect('section_unit_list', self.section.id)

        return self.render_to_response({
            'form': form, 'object': self.obj
        })


class UnitDeleteView(View):

    def post(self, request, unit_id):
        unit = get_object_or_404(Unit, id=unit_id,
                                 section__course__author=request.user)
        section = unit.section
        unit.item.delete()
        unit.delete()
        return redirect('section_unit_list', section.id)


class SectionUnitListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/section/unit_list.html'

    def get(self, request, section_id):
        section = get_object_or_404(Section, id=section_id,
                                    course__author=request.user)
        return self.render_to_response({
            'section': section
        })


class SectionOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request):
        for id, order in self.request_json.items():
            Section.objects.filter(
                id=id, course__author=request.author).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class UnitOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request):
        for id, order in self.request_json.items():
            Unit.objects.filter(
                id=id, section__course__author=request.user,
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})
