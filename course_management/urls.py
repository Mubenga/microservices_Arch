from django.contrib import admin
from django.urls import path, include
from .views import redirect_to_api  # Import your custom redirect view

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API URLs for the courses
    path('api/', include(('courses.api.urls', 'courses.api'), namespace='api')),
    
    # Redirect root URL to /api/
    path('', redirect_to_api, name='redirect_to_api'),
]
