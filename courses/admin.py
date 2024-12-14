from django.contrib import admin
from .models import Subject, Course, Module

admin.site.index_template = 'memcache_status/admin_index.html'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {"slug": ('title',)}


class ModuleInline(admin.TabularInline):  # Switched to TabularInline for compact display
    model = Module
    extra = 1  # Display one empty form for adding new modules


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    readonly_fields = ['created']  # Make created read-only


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):  # Optional: Separate management of Module in admin
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'description']
