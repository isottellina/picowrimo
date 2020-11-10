from django.contrib.auth.models import User
from rest_framework import viewsets, authentication, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Project, Advancement
from .serializers import ProjectSerializer, AdvancementSerializer, UserSerializer
from .forms import AdvancementFilter

class DefaultsMixin(object):
    """
    Default settings for view authentication, permissions,
    filtering and pagination.
    """
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

class ProjectViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Project.objects.order_by('name')
    serializer_class = ProjectSerializer
    search_fields = ('name', 'description')
    ordering_fields = ('name')

class AdvancementViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Advancement.objects
    serializer_class = AdvancementSerializer
    filter_class = AdvancementFilter

class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = (User.USERNAME_FIELD, )