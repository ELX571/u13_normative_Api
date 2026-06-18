from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts import views
from accounts.views import AuthWithToken

router = DefaultRouter()
router.register('auth', views.AuthAPIView, basename='auth')
router.register('auth-token',AuthWithToken,basename='auth-token')

urlpatterns = router.urls
