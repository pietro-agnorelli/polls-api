from rest_framework import serializers
from .models import PollsUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=PollsUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = PollsUser
        fields = ('username', 'password', 'password2', 'email', 'bio', 'gender')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        password=validated_data['password']
        del validated_data['password']
        user = PollsUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user