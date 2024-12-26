from rest_framework.decorators import action
from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from ..models import Subject, Course, Module
from .serializers import (
    SubjectSerializer,
    CourseSerializer,
    CourseWithContentSerializer,
    ModuleSerializer,
    ContentSerializer
)
from .permissions import IsEnrolled


class SubjectListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating subjects.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SubjectDetailView(generics.RetrieveAPIView):
    """
    Returns detailed information about a specific subject.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    """
    A viewset for retrieving course details and handling enrollments.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
        detail=True,
        methods=['get'],
        serializer_class=CourseWithContentSerializer,
        permission_classes=[IsAuthenticated, IsEnrolled]
    )
    def contents(self, request, *args, **kwargs):
        """
        Returns detailed course content for enrolled students.
        """
        return self.retrieve(request, *args, **kwargs)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        """
        Allows a user to enroll in a course.
        """
        course = self.get_object()
        course.students.add(request.user)  # Adjust this to add `request.user.id` if necessary
        return Response({'enrolled': True}, status=status.HTTP_200_OK)


class ModuleListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating modules.
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ModuleViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing individual modules.
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific module by its primary key.
        """
        try:
            module = self.get_object()
            serializer = self.get_serializer(module)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Module.DoesNotExist:
            raise NotFound('Module not found')