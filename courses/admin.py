from django.contrib import admin
from courses.models import Subject, Course, Section, Unit

# Register your models here.
admin.site.register(Section)
admin.site.register(Unit)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_display_links = ['title', 'slug']
    # list_editable = ['title']
    fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', )}
    actions_on_bottom = True


class SectionInline(admin.StackedInline):
    model = Section


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SectionInline]

