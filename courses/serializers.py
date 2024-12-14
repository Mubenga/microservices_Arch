# courses/api/serializers.py
from rest_framework import serializers
from .models import Course
from .models import Module

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'overview', 'slug', 'created', 'subject', 'owner_id', 'students', 'payment_status']



class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'course', 'title', 'description', 'order']
