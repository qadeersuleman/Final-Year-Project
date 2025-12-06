from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    qualification = models.TextField()
    experience = models.IntegerField()
    license_number = models.CharField(max_length=50)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Use full_name field instead of first_name/last_name
        user = self.user
        
        # Get display name from full_name, username, or email
        if user.full_name and user.full_name.strip():
            display_name = user.full_name
        elif user.username:
            display_name = user.username
        elif user.email:
            display_name = user.email.split('@')[0]  # Use email username part
        else:
            display_name = f"Doctor-{self.id}"
        
        return f"Dr. {display_name} - {self.specialization}"
    
    def get_full_display_name(self):
        """Alternative method to get just the doctor's name without specialization"""
        user = self.user
        
        # Try to get a proper display name
        if user.full_name and user.full_name.strip():
            return f"Dr. {user.full_name}"
        elif user.username:
            return f"Dr. {user.username}"
        elif user.email:
            return f"Dr. {user.email.split('@')[0]}"
        else:
            return f"Dr. {self.id}"




class AvailabilitySchedule(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration = models.IntegerField(default=60)  # in minutes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    meeting_id = models.CharField(max_length=100, blank=True)  # For video calls
    
    class Meta:
        unique_together = ['doctor', 'appointment_date', 'appointment_time']




class AppointmentNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50)  # reminder, cancellation, etc.





from django.db import models
from django.conf import settings

class VideoCallSession(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)  # ✅ Fix this
    room_id = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"VideoCall: {self.room_id}"





class CallLog(models.Model):
    session = models.ForeignKey(VideoCallSession, on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)