import datetime
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from . import serializers
from .utils import get_and_authenticate_user, create_user_account
from questions.serializers import (
    QuestionSerializer, AnswerSerializer
)
from questions.models import Question, Answer

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer
    }

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.UserSerializer(user).data
        data['last_login'] = datetime.datetime.now()
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializers.UserRegisterSerializer(user).data
        data['last_login'] = datetime.datetime.now()
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Question.objects.filter(user_id=self.kwargs['user_id'])


class AnswerList(generics.ListAPIView):
    serializer_class = AnswerSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Answer.objects.filter(user_id=self.kwargs['user_id'])


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    lookup_url_kwarg = 'question_id'

    def get_queryset(self):
        return Question.objects.filter(user_id=self.kwargs['user_id'])


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    lookup_url_kwarg = 'answer_id'

    def get_queryset(self):
        return Answer.objects.filter(user_id=self.kwargs['user_id'])
