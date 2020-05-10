from django.db.models import Count
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    TagSerializer
)
from .models import Question, Answer
from taggit.models import Tag


class QuestionViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['id', 'likes', 'views']
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def retrieve(self, request, *args, **kwargs):
        question = self.get_object()
        question.views += 1
        question.save(update_fields=("views", ))
        return super().retrieve(request, *args, **kwargs)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class OpenQuestionListView(generics.ListAPIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['id', 'likes', 'views']
    pagination_class = PageNumberPagination
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = (Question.objects
                    .select_related('user')
                    .prefetch_related('answers', 'tags')
                    )
        queryset_ids = [
            obj.id for obj in queryset if not obj.get_accepted_answer()
        ]
        queryset = queryset.filter(id__in=queryset_ids)
        return queryset


class SolvedQuestionListView(generics.ListAPIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['id', 'likes', 'views']
    serializer_class = QuestionSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = (Question.objects
                    .select_related('user')
                    .prefetch_related('answers', 'tags')
                    )
        queryset_ids = [
            obj.id for obj in queryset if obj.get_accepted_answer()
        ]
        queryset = queryset.filter(id__in=queryset_ids)
        return queryset


class TagListView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(
            tags__slug=self.kwargs.get("slug")
        ).all()


class CategoryListView(generics.ListAPIView):
    serializer_class = TagSerializer
    pagination_class = None

    def get_queryset(self):
        return Tag.objects.all().annotate(
            count_tags=Count('taggit_taggeditem_items')
        )
