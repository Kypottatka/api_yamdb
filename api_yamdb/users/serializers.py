import re

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        email = data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email '
                'уже существует'
            )
        return data

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'bio',
            'role',
        )
        lookup_field = 'username'
        extra_kwargs = {
            'email': {'required': True},
            'url': {'lookup_field': 'username'},
        }


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя!'
            )
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError(
                'Имя пользователя должно состоять '
                'только из букв латинского алфавита, '
                'цифр и символов "@/./+/-/_"'
            )
        return username

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
