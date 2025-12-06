from django.contrib import admin
from .models import Doctor, AvailabilitySchedule, Appointment, AppointmentNotification

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_display_name', 'specialization', 'is_verified', 'is_online', 'created_at']
    list_filter = ['specialization', 'is_verified', 'is_online']
    search_fields = ['user__full_name', 'user__username', 'user__email', 'specialization']
    
    def get_display_name(self, obj):
        return obj.get_full_display_name()
    
    get_display_name.short_description = 'Doctor Name'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_display', 'doctor_display', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date']
    search_fields = [
        'patient__full_name', 'patient__username', 'patient__email',
        'doctor__user__full_name', 'doctor__user__username', 'doctor__user__email'
    ]
    
    def patient_display(self, obj):
        # Display patient name nicely using full_name
        user = obj.patient
        if user.full_name and user.full_name.strip():
            return user.full_name
        elif user.username:
            return user.username
        return user.email.split('@')[0] if user.email else f"User-{user.id}"
    
    def doctor_display(self, obj):
        # Use the doctor's display method
        return obj.doctor.get_full_display_name()
    
    patient_display.short_description = 'Patient'
    doctor_display.short_description = 'Doctor'

@admin.register(AvailabilitySchedule)
class AvailabilityScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor_display', 'get_day_of_week_display', 'start_time', 'end_time', 'is_available']
    list_filter = ['day_of_week', 'is_available']
    
    def doctor_display(self, obj):
        return obj.doctor.get_full_display_name()
    
    def get_day_of_week_display(self, obj):
        return obj.get_day_of_week_display()
    
    doctor_display.short_description = 'Doctor'
    get_day_of_week_display.short_description = 'Day'

@admin.register(AppointmentNotification)
class AppointmentNotificationAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'appointment', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
    
    def user_display(self, obj):
        user = obj.user
        if user.full_name and user.full_name.strip():
            return user.full_name
        elif user.username:
            return user.username
        return user.email.split('@')[0] if user.email else f"User-{user.id}"
    
    user_display.short_description = 'User'