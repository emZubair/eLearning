from django.contrib import admin
from courses.models import Subject, Course, Section

# Register your models here.


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', )}


class SectionInline(admin.StackedInline):
    model = Section


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SectionInline]

