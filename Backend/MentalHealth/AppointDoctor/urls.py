from django.urls import path
from .views import (
    CreateVideoCallSession, JoinVideoCall, LeaveVideoCall, 
    EndVideoCallSession, UserAppointmentsAPI, UpcomingAppointmentsAPI,
    my_appointments_api, CreateVideoCallAPI, CheckDoctorAvailability,
    SimpleVideoCallAPI,DoctorsListAPI,CreateAppointmentAPI
)

urlpatterns = [
    # Video Call URLs
    path('create-session/', CreateVideoCallSession.as_view(), name='create_session'),
    path('join-call/', JoinVideoCall.as_view(), name='join_call'),
    path('leave-call/', LeaveVideoCall.as_view(), name='leave_call'),
    path('end-session/', EndVideoCallSession.as_view(), name='end_session'),
    path('check-availability/<int:appointment_id>/', CheckDoctorAvailability.as_view(), name='check_availability'),
    path('simple-create/', SimpleVideoCallAPI.as_view(), name='simple_video_call'),
    
    # Appointment URLs
    path('user-appointments/', UserAppointmentsAPI.as_view(), name='user_appointments'),
    path('upcoming-appointments/', UpcomingAppointmentsAPI.as_view(), name='upcoming_appointments'),
    path('my-appointments/', my_appointments_api, name='my_appointments'),
    path('create-video-call/', CreateVideoCallAPI.as_view(), name='create_video_call'),

    # New URLs for doctors and appointments
    path('doctors/', DoctorsListAPI.as_view(), name='doctors_list'),
    path('create-appointment/', CreateAppointmentAPI.as_view(), name='create_appointment'),
]