from django import forms
from django.forms.models import inlineformset_factory

from courses.models import Course, Section


ModuleFormSet = inlineformset_factory(Course, Section,
                                      fields=['title', 'description'],
                                      extra=2,
                                      can_delete=True)
