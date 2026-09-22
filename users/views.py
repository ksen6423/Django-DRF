from rest_framework.generics import RetrieveUpdateAPIView

from users.models import User
from users.serializer import UserSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
