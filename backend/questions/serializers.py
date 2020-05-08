from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit_serializer.serializers import (
    TagListSerializerField,
    TaggitSerializer
)
from taggit.models import Tag
from .models import Question, Answer


User = get_user_model()


class AnswerSerializer(serializers.ModelSerializer):
    answer_author = serializers.ReadOnlyField(source='user.username')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):
    question_author = serializers.ReadOnlyField(source='user.username')
    answers = AnswerSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tags = TagListSerializerField()

    class Meta:
        model = Question
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
