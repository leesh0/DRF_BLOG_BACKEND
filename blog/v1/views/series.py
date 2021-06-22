from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.mixins import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, response, status, authentication, exceptions
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import permission_classes
from rest_framework.generics import *
from blog.models import *
from blog.v1.serializers.series import *


# Create your views here.


class SeriesView(ListCreateAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        obj = Series.objects.all()
        return obj \
            .select_related('author') \
            .prefetch_related('post')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserSeriesView(ListAPIView):
    serializer_class = SeriesSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        author = self.kwargs.get('author')
        slug = self.request.data.get('slug')
        return Series.objects.filter(author__username=author)\
            .select_related('author')\
            .prefetch_related('post')

class UserDetailSeriesView(RetrieveUpdateDestroyAPIView):
    serializer_class = SeriesDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "author"

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset)

    def get_queryset(self):
        author = self.kwargs.get('author')
        slug = self.kwargs.get('slug')
        return Series.objects.filter(author__username=author, slug=slug)\
            .select_related('author')\
            .prefetch_related('post')
