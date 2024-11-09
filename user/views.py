from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

User = get_user_model()  # Use get_user_model to get the custom user model


class UserViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only for listing and retrieving user info
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
