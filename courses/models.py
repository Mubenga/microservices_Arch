from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Student(models.Model):
    # Minimal information to link with the Auth service
    user_id = models.PositiveIntegerField(unique=True)  # Unique user ID from Auth service
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Student {self.user_id}'


class Course(models.Model):
    owner_id = models.PositiveIntegerField()  # Store user ID from the external Auth service
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)  # Changed to `SlugField` for better validation
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, related_name="courses_joined", blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('paid', 'Paid')],
        default='pending'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module, related_name="contents", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ('text', 'video', 'image', 'file')}
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    image = models.ImageField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
