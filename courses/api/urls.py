
# in courses/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import SubjectListCreateView, SubjectDetailView  # Ensure this is correct
from .views import ModuleListCreateView
from .views import ModuleViewSet

# Define the router and register the CourseViewSet
router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

# Namespace for the API app
app_name = 'courses.api'

# URL patterns
urlpatterns = [
    path('subjects/', SubjectListCreateView.as_view(), name='subject_list_create'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('', include(router.urls)),
    path('modules/', ModuleListCreateView.as_view(), name='module_list_create'),
    path('modules/<int:pk>/', ModuleViewSet.as_view({'get': 'retrieve'}), name='module-detail'),
  
]
