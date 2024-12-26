from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    """
    Custom permission to check if a user is enrolled in a course.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the requesting user is enrolled in the course object.
        """
        if hasattr(request, 'user') and getattr(request.user, 'is_authenticated', False):
            # Assuming obj.students stores a ManyToMany relationship with Student model
            return obj.students.filter(user_id=request.user.id).exists()
        return False
