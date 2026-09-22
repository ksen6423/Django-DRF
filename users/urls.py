from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserRetrieveUpdateAPIView, UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("users/profile/", UserRetrieveUpdateAPIView.as_view(), name="users_profile"),
]
