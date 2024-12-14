from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """
    Custom permission to check if a user is enrolled in a course.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the requesting user is enrolled in the course object.
        """
        if request.user.is_authenticated:
            return obj.students.filter(id=request.user.id).exists()
        return False
