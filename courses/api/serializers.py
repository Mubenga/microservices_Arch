from rest_framework import serializers
from ..models import Subject, Course, Module, Content, Text, File, Image, Video


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'course', 'title', 'description', 'order']

    def validate_course(self, value):
        """
        Ensure the course exists before creating a module.
        """
        if not Course.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("The specified course does not exist.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner_id', 'students', 'modules']


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        """
        Render different content types based on their model.
        """
        if isinstance(value, Text):
            return {"type": "text", "content": value.content}
        elif isinstance(value, File):
            return {"type": "file", "file": value.file.url}
        elif isinstance(value, Image):
            return {"type": "image", "image": value.image.url}
        elif isinstance(value, Video):
            return {"type": "video", "url": value.url}
        else:
            return {"type": "unknown", "content": str(value)}


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'order', 'item']


class ModuleWithContentSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['id', 'order', 'title', 'description', 'contents']


class CourseWithContentSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'students', 'modules']

