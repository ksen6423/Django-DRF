from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def validate_email(self, value):
            if User.objects.filter(email__iexact=value).exists():
                raise serializers.ValidationError("Пользователь с таким Email уже существует.")
            return value


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
