from rest_framework.decorators import action
from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Module
from .serializers import ModuleSerializer
from rest_framework.generics import RetrieveAPIView

from rest_framework import status
from .serializers import ContentSerializer


from rest_framework.exceptions import NotFound


from ..models import Subject, Course
from .serializers import (
    SubjectSerializer, 
    CourseSerializer, 
    CourseWithContentSerializer
)
from .permissions import IsEnrolled


class SubjectListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating subjects.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    


class SubjectDetailView(generics.RetrieveAPIView):
    """
    Returns detailed information about a specific subject.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    A viewset for retrieving course details and handling enrollments.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(
        detail=True,
        methods=['get'],
        serializer_class=CourseWithContentSerializer,
        authentication_classes=[BasicAuthentication],
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
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        """
        Allows a user to enroll in a course.
        """
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

class ModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def retrieve(self, request, pk=None):
        try:
            module = self.get_object()
            serializer = self.get_serializer(module)
            return Response(serializer.data)
        except Module.DoesNotExist:
            raise NotFound('Module not found')
        
