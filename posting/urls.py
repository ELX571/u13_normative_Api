from django.urls import path

from posting import views

urlpatterns = [
    path('salom-api/',views.salomApiView,name='salom'),
    path('post/', views.PostApiView.as_view(),name='post'),
    path('post/<int:pk>/',views.PostDetailApiView.as_view(),name='detail'),
]