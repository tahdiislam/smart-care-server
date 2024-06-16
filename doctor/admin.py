from django.contrib import admin
from .models import Doctor, Specialization, Designation, AvailableTime, Review
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Specialization)
admin.site.register(Designation)
admin.site.register(AvailableTime)
admin.site.register(Review)