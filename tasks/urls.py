from django.urls import path

from tasks import views

urlpatterns = [
    path('salom-api/',views.salomApiView,name='salom'),
]