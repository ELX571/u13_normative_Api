from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posting import views

router = DefaultRouter()
router.register(r'posts-viewset', views.PostViewSet, basename='post-viewset')
router.register(r'posts-modelviewset', views.PostModelViewSet, basename='post-modelviewset')
router.register(r'posts', views.PostModelViewSet, basename='posts')

urlpatterns = [
    path('salom-api/',views.salomApiView,name='salom'),
    path('post/', views.PostApiView.as_view(),name='post'),
    path('post/<int:pk>/',views.PostDetailApiView.as_view(),name='detail'),
    path('', include(router.urls)),
]