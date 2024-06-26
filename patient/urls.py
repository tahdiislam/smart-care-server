from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('list', views.PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]