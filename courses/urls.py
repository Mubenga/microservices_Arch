from django.urls import path
from . import views

urlpatterns = [
    # Manage teacher's courses
    path('mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),

    # Create a new course
    path('create/', views.CourseCreateView.as_view(), name='course_create'),

    # Edit an existing course
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),

    # Delete an existing course
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # Manage modules of a course
    path('<int:pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),

    # Add a new content (text, image, video, file) to a module
    path('module/<int:module_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(),
         name='module_content_create'),

    # Edit a content item of a module
    path('module/<int:module_id>/content/<model_name>/<int:id>/', views.ContentCreateUpdateView.as_view(),
         name='module_content_update'),

    # Delete a content item from a module
    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),

    # Manage content within a module
    path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),

    # Reorder modules
    path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),

    # Reorder contents
    path('content/order/', views.ContentOrderView.as_view(), name='content_order'),

    # List all courses under a specific subject
    path('subject/<slug:subject>/', views.CourseListView.as_view(), name='course_list_subject'),

    # View details of a specific course (enroll page)
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]
