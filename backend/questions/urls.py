from django.urls import path
from rest_framework import routers
from .views import (
    QuestionViewSet,
    AnswerViewSet,
    TagListView,
    CategoryListView
)
router = routers.DefaultRouter(trailing_slash=False)
router.register('questions', QuestionViewSet, basename='questions')
router.register('answers', AnswerViewSet, basename='answers')


urlpatterns = router.urls

urlpatterns += [
    path('tags/<str:slug>', TagListView.as_view()),
    path('categories', CategoryListView.as_view())
]
