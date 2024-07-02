from typing import Any
from django.contrib import admin
from .models import Appointment
#for sending mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'patient_name', 'time')

    def doctor_name(self, obj):
        return obj.doctor.user.first_name + " " + obj.doctor.user.last_name

    def patient_name(self, obj):
        return obj.patient.user.first_name + " " + obj.patient.user.last_name
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.save()
        if obj.appointment_status == "Running" and obj.appointment_type == "Online":
            email_subject = 'Your Online Appointment is confirmed'
            email_body = render_to_string('appointment/appointment_confirm_mail.html',{'user': obj.patient.user, 'doctor': obj.doctor.user})
            email = EmailMultiAlternatives(email_subject, '', to=[obj.patient.user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            

admin.site.register(Appointment, AppointmentAdmin)