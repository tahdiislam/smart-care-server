from django.shortcuts import render
from .serializers import AppointmentSerializer
from .models import Appointment
from rest_framework import viewsets

# Create your views here.
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer