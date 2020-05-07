from rest_framework import routers
from accounts.views import (
    AuthViewSet,
    UserViewSet
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('api/users', UserViewSet, basename='users')

urlpatterns = router.urls
