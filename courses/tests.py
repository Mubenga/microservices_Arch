# courses/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import Subject, Course, Module, Student

# courses/tests.py
class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.subject = Subject.objects.create(title='Test Subject', slug='test-subject')
        self.student = Student.objects.create(user_id=1)
        self.course = Course.objects.create(subject=self.subject, title='Test Course', slug='test-course', overview='Test Overview', owner_id=1)
        self.module = Module.objects.create(course=self.course, title='Test Module', description='Test Description', order=1)
        self.valid_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3NjVjNzdmYTc0OGFhYjM4NTBjMjVjOCIsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsImlhdCI6MTczNDcyNDE2MiwiZXhwIjoxNzM0NzI3NzYyfQ.bGrP5utor_7wNVwRp1WxCP5Q1cYGVHAPcxWsrp-XHuA'  # Replace with a valid token
        self.invalid_token = 'invalid_jwt_token'
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.valid_token}',
        }

    # Test cases...

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.subject = Subject.objects.create(title='Test Subject', slug='test-subject')
        self.student = Student.objects.create(user_id=1)
        self.course = Course.objects.create(subject=self.subject, title='Test Course', slug='test-course', overview='Test Overview', owner_id=1)
        self.module = Module.objects.create(course=self.course, title='Test Module', description='Test Description', order=1)
        self.valid_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3NjVjNzdmYTc0OGFhYjM4NTBjMjVjOCIsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsImlhdCI6MTczNDcyNDE2MiwiZXhwIjoxNzM0NzI3NzYyfQ.bGrP5utor_7wNVwRp1WxCP5Q1cYGVHAPcxWsrp-XHuA'  # Replace with a valid token
        self.invalid_token = 'invalid_jwt_token'
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.valid_token}',
        }

    def test_subject_list(self):
        response = self.client.get(reverse('api:subject_list_create'), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subject_detail(self):
        response = self.client.get(reverse('api:subject_detail', args=[self.subject.id]), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_list(self):
        response = self.client.get(reverse('api:course-list'), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_detail(self):
        response = self.client.get(reverse('api:course-detail', args=[self.course.id]), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        data = {
            'subject': self.subject.id,
            'title': 'New Course',
            'slug': 'new-course',
            'overview': 'New Overview',
            'owner_id': 1
        }
        response = self.client.post(reverse('api:course-list'), data, content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_course(self):
        data = {
            'subject': self.subject.id,
            'title': 'Updated Course',
            'slug': 'updated-course',
            'overview': 'Updated Overview',
            'owner_id': 1
        }
        response = self.client.put(reverse('api:course-detail', args=[self.course.id]), data, content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        response = self.client.delete(reverse('api:course-detail', args=[self.course.id]), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_enroll_course(self):
        response = self.client.post(reverse('api:course-enroll', args=[self.course.id]), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_contents(self):
        response = self.client.get(reverse('api:course-contents', args=[self.course.id]), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_module_list(self):
        response = self.client.get(reverse('api:module_list_create'), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_module_detail(self):
        response = self.client.get(reverse('api:module-detail', args=[self.module.id]), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_module(self):
        data = {
            'course': self.course.id,
            'title': 'New Module',
            'description': 'New Description',
            'order': 2
        }
        response = self.client.post(reverse('api:module_list_create'), data, content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_module(self):
        data = {
            'course': self.course.id,
            'title': 'Updated Module',
            'description': 'Updated Description',
            'order': 1
        }
        response = self.client.put(reverse('api:module-detail', args=[self.module.id]), data, content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_module(self):
        response = self.client.delete(reverse('api:module-detail', args=[self.module.id]), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_token(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.invalid_token}',
        }
        response = self.client.get(reverse('api:course-list'), **headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)