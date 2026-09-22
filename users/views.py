from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializer import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
