from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'service_type', 'user', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('service_type', 'status', 'appointment_date')
    search_fields = ('pet_name', 'user__username')
    list_editable = ('status',)
