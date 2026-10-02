from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserRetrieveUpdateAPIView, UserViewSet, UserCreateAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("users/profile/", UserRetrieveUpdateAPIView.as_view(), name="user-profile"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path('', include(router.urls)),
]
