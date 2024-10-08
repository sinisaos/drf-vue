from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise serializers.ValidationError(
            "Invalid username/password. Please try again!"
        )
    return user


def create_user_account(email, password, **extra_fields):
    user = get_user_model().objects.create_user(
        email=email, password=password, **extra_fields
    )
    return user
