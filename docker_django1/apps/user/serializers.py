from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from docker_django1.apps.user.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    email = serializers.EmailField(max_length=255, required=True, label='Email')
    first_name = serializers.CharField(max_length=255, required=True, label='Имя')
    last_name = serializers.CharField(max_length=255, required=True, label='Отчество')
    middle_name = serializers.CharField(max_length=255, required=False, label='Фамилия')
    email_verified = serializers.BooleanField()
    password = serializers.CharField(
        min_length=4,
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Пароль',
    )

    class Meta:
        fields = '__all__'
        model = User

    def create(self, validated_data):
        user = self.Meta.model.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def validate(self, attrs):
        """todo добавить валидацию по ФИО (отчество опционально,
        сделать trim whitespaces (можно в самом сериализаторе))"""
        data = super(UserSerializer, self).validate(attrs)
        if User.objects.filter(email__iexact=data['email']).exists():
            raise ValidationError(
                code=f'user_already_registered',
                detail=f'Пользователь c таким email "{data["email"]}" уже существует',
            )
        return data
