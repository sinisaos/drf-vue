from django.urls import path
from rest_framework import routers
from accounts.views import (
    AuthViewSet,
    UserViewSet,
    QuestionList,
    AnswerList,
    QuestionDetail,
    AnswerDetail
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('api/users', UserViewSet, basename='users')

urlpatterns = router.urls

urlpatterns += [
    path('api/users/<int:user_id>/questions', QuestionList.as_view()),
    path(
        'api/users/<int:user_id>/questions/<int:question_id>',
        QuestionDetail.as_view()
    ),
    path('api/users/<int:user_id>/answers', AnswerList.as_view()),
    path(
        'api/users/<int:user_id>/answers/<int:answer_id>',
        AnswerDetail.as_view()
    ),
]
