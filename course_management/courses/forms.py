from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

ModuleFormSet = inlineformset_factory(
    Course,  # Parent model
    Module,  # Related model
    fields=['title', 'description'],  # Fields to include in the form
    extra=2,  # Number of empty forms to display
    can_delete=True  # Allow deletion of associated modules
)
