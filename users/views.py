from requests import session
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, CoursePayment

from users.models import User
from users.serializer import UserSerializer, PaymentSerializer, CoursePaymentSerializer
from .services import create_stripe_price, create_stripe_session


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ["course", "lesson", "payment_method"]

    ordering_fields = ["payment_date"]


class CoursePaymentCreateAPIView(CreateAPIView):
    queryset = CoursePayment.objects.all()
    serializer_class = CoursePaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
