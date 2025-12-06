from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import string
from .models import VideoCallSession, CallLog, Appointment
from django.utils import timezone
from datetime import timedelta







@method_decorator(csrf_exempt, name='dispatch')
class CreateVideoCallSession(APIView):
    def post(self, request):
        try:
            appointment_id = request.data.get('appointment_id')
            user_id = request.data.get('user_id')
            
            print(f"🎥 Creating video call for appointment: {appointment_id}, user: {user_id}")
            
            if not appointment_id or not user_id:
                return Response({
                    'success': False,
                    'error': 'appointment_id and user_id are required'
                }, status=400)
            
            # Check if appointment exists and is confirmed
            try:
                appointment = Appointment.objects.get(
                    id=appointment_id, 
                    status='confirmed'
                )
            except Appointment.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Confirmed appointment not found'
                }, status=404)
            
            # ✅ Simple room ID generation
            room_id = f"room_{appointment_id}_{user_id}_{random.randint(1000, 9999)}"
            
            # Create video call session
            session, created = VideoCallSession.objects.get_or_create(
                appointment=appointment,
                defaults={
                    'room_id': room_id,
                    'is_active': True
                }
            )
            
            # If session already exists, use existing room_id
            if not created:
                room_id = session.room_id
            
            return Response({
                'success': True,
                'room_id': room_id,
                'appointment_id': appointment.id,
                'doctor_name': f"Dr. {appointment.doctor.user.get_full_name()}",
                'patient_name': appointment.patient.get_full_name(),
                'session_id': session.id
            })
            
        except Exception as e:
            print(f"❌ Error creating video call: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)



@method_decorator(csrf_exempt, name='dispatch')
class JoinVideoCall(APIView):
    def post(self, request):
        try:
            room_id = request.data.get('room_id')
            user_id = request.data.get('user_id')
            
            session = VideoCallSession.objects.get(room_id=room_id, is_active=True)
            
            # Create call log entry
            call_log = CallLog.objects.create(
                session=session,
                participant_id=user_id
            )
            
            return Response({
                'success': True,
                'room_id': room_id,
                'call_log_id': call_log.id,
                'message': 'Successfully joined video call'
            })
            
        except VideoCallSession.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Video call session not found or inactive'
            }, status=404)








@method_decorator(csrf_exempt, name='dispatch')
class LeaveVideoCall(APIView):
    def post(self, request):
        try:
            call_log_id = request.data.get('call_log_id')
            
            call_log = CallLog.objects.get(id=call_log_id)
            call_log.left_at = timezone.now()
            
            # Calculate duration in seconds
            duration = (call_log.left_at - call_log.joined_at).total_seconds()
            call_log.duration = int(duration)
            
            call_log.save()
            
            return Response({
                'success': True,
                'duration': call_log.duration
            })
            
        except CallLog.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Call log not found'
            }, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class EndVideoCallSession(APIView):
    def post(self, request):
        try:
            room_id = request.data.get('room_id')
            
            session = VideoCallSession.objects.get(room_id=room_id)
            session.is_active = False
            session.save()
            
            return Response({
                'success': True,
                'message': 'Video call session ended'
            })
            
        except VideoCallSession.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Video call session not found'
            }, status=404)
        



from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Appointment, Doctor
from django.utils import timezone
from django.db.models import Q

class UserAppointmentsAPI(APIView):
    
    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            user_role = request.GET.get('user_role')  # 'patient' or 'doctor' or 'user'
            
            print(f"📱 UserAppointmentsAPI - user_id: {user_id}, user_role: {user_role}")  # Debug
            
            if not user_id or not user_role:
                return Response({
                    'success': False,
                    'error': 'user_id and user_role are required'
                }, status=400)
            
            # ✅ FIX 1: 'user' role ko bhi 'patient' ki tarah treat karo
            if user_role in ['patient', 'user']:
                appointments = Appointment.objects.filter(
                    patient_id=user_id
                ).select_related('doctor', 'doctor__user').order_by('-appointment_date', '-appointment_time')
                
                print(f"✅ Patient appointments found: {appointments.count()}")  # Debug
                
            elif user_role == 'doctor':
                # Doctor ke appointments ke liye
                appointments = Appointment.objects.filter(
                    doctor_id=user_id
                ).select_related('patient', 'doctor__user').order_by('-appointment_date', '-appointment_time')
                
                print(f"✅ Doctor appointments found: {appointments.count()}")  # Debug
            else:
                return Response({
                    'success': False,
                    'error': f'Invalid user role: {user_role}. Must be patient, user or doctor'
                }, status=400)
            
            appointments_data = []
            for appointment in appointments:
                appointment_data = {
                    'id': appointment.id,
                    'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
                    'appointment_time': appointment.appointment_time.strftime('%H:%M'),
                    'status': appointment.status,
                    'duration': appointment.duration,
                    'symptoms': appointment.symptoms,
                    'notes': appointment.notes,
                    'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M'),
                }
                
                # ✅ FIX 2: 'user' role ke liye bhi doctor information provide karo
                if user_role in ['patient', 'user']:
                    appointment_data['doctor_name'] = f"Dr. {appointment.doctor.user.get_full_name()}"
                    appointment_data['doctor_specialization'] = appointment.doctor.specialization
                    appointment_data['patient_name'] = f"{appointment.patient.get_full_name()}"  # ✅ Add patient name bhi
                else:
                    appointment_data['patient_name'] = appointment.patient.get_full_name()
                    appointment_data['doctor_name'] = f"Dr. {appointment.doctor.user.get_full_name()}"  # ✅ Doctor ke liye bhi
                
                appointments_data.append(appointment_data)
            
            print(f"✅ Total appointments to return: {len(appointments_data)}")  # Debug
            
            return Response({
                'success': True,
                'appointments': appointments_data,
                'count': len(appointments_data),
                'user_role_received': user_role,
                'user_role_used': 'patient' if user_role in ['patient', 'user'] else 'doctor'  # Debug info
            })
            
        except Exception as e:
            print(f"❌ Error in UserAppointmentsAPI: {str(e)}")  # Debug
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)



class UpcomingAppointmentsAPI(APIView):
    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            user_role = request.GET.get('user_role')
            
            print(f"Received request - user_id: {user_id}, user_role: {user_role}")  # Debug
            
            if not user_id or not user_role:
                return Response({
                    'success': False,
                    'error': 'user_id and user_role are required'
                }, status=400)
            
            # ✅ 'user' role ko bhi accept karo aur 'patient' treat karo
            valid_roles = ['patient', 'doctor', 'user']  # 'user' ko bhi allow karo
            if user_role not in valid_roles:
                return Response({
                    'success': False,
                    'error': f'Invalid user role: {user_role}. Must be one of: {valid_roles}'
                }, status=400)
            
            today = timezone.now().date()
            
            # ✅ 'user' role ko automatically 'patient' treat karo
            if user_role in ['patient', 'user']:
                appointments = Appointment.objects.filter(
                    patient_id=user_id,
                    appointment_date__gte=today,
                    status__in=['scheduled', 'confirmed']
                ).select_related('doctor', 'doctor__user').order_by('appointment_date', 'appointment_time')
            elif user_role == 'doctor':
                appointments = Appointment.objects.filter(
                    doctor_id=user_id,
                    appointment_date__gte=today,
                    status__in=['scheduled', 'confirmed']
                ).select_related('patient', 'doctor__user').order_by('appointment_date', 'appointment_time')
            
            appointments_data = []
            for appointment in appointments:
                appointment_data = {
                    'id': appointment.id,
                    'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
                    'appointment_time': appointment.appointment_time.strftime('%H:%M'),
                    'status': appointment.status,
                    'duration': appointment.duration,
                    'symptoms': appointment.symptoms,
                }
                
                # ✅ 'user' role ke liye bhi doctor information provide karo
                if user_role in ['patient', 'user']:
                    appointment_data['doctor_name'] = f"Dr. {appointment.doctor.user.get_full_name()}"
                    appointment_data['doctor_specialization'] = appointment.doctor.specialization
                    appointment_data['patient_name'] = appointment.patient.get_full_name()
                else:
                    appointment_data['patient_name'] = appointment.patient.get_full_name()
                    appointment_data['doctor_name'] = f"Dr. {appointment.doctor.user.get_full_name()}"
                
                appointments_data.append(appointment_data)
            
            print(f"Found {len(appointments_data)} appointments")  # Debug
            
            return Response({
                'success': True,
                'appointments': appointments_data,
                'count': len(appointments_data),
                'user_role_received': user_role,  # Debug ke liye
                'user_role_used': 'patient' if user_role in ['patient', 'user'] else 'doctor'  # Debug ke liye
            })
            
        except Exception as e:
            print(f"Error in UpcomingAppointmentsAPI: {str(e)}")  # Debug
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)


# Test appointments create karne ke liye (temporary)
class CreateTestAppointment(APIView):
    def post(self, request):
        try:
            from django.contrib.auth.models import User
            from datetime import date, time
            
            # Test patient aur doctor get karo
            patient = User.objects.get(id=request.data.get('patient_id', 6))  # Your user ID
            doctor = Doctor.objects.first()  # First available doctor
            
            if not doctor:
                return Response({'error': 'No doctor available'}, status=400)
            
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=date.today(),
                appointment_time=time(10, 0),
                duration=60,
                status='confirmed',
                symptoms='Test symptoms for video call'
            )
            
            return Response({
                'success': True,
                'appointment_id': appointment.id,
                'message': 'Test appointment created successfully'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
        




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Appointment
import json



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import Appointment, Doctor
import json

print("My appointments API initialized")

# Get the custom user model
User = get_user_model()

def get_user_display_name(user):
    """Helper function to get display name from custom user model"""
    if user.full_name and user.full_name.strip():
        return user.full_name
    elif user.username:
        return user.username
    elif user.email:
        return user.email.split('@')[0]
    else:
        return f"User-{user.id}"

def get_doctor_display_name(doctor):
    """Helper function to get doctor display name"""
    if doctor.user.full_name and doctor.user.full_name.strip():
        return f"Dr. {doctor.user.full_name}"
    elif doctor.user.username:
        return f"Dr. {doctor.user.username}"
    elif doctor.user.email:
        return f"Dr. {doctor.user.email.split('@')[0]}"
    else:
        return f"Dr. {doctor.id}"

@csrf_exempt
@api_view(['POST'])
def my_appointments_api(request):
    """
    Function-based view to get appointments for user
    Receives user_id in request body (POST method)
    """
    try:
        data = request.data
        user_id = data.get('user_id')
        
        if not user_id:
            print("❌ No user_id provided in request body")
            return Response({
                'success': False,
                'error': 'User ID is required',
                'detail': 'Please provide user_id in request body'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get user by ID using the custom user model
            user = User.objects.get(id=int(user_id))
            # Use helper function to get display name
            user_display_name = get_user_display_name(user)
            print(f"📱 Fetching appointments for user: {user.id} - {user_display_name}")
        except User.DoesNotExist:
            print(f"❌ User not found: {user_id}")
            return Response({
                'success': False,
                'error': 'User not found',
                'detail': 'Invalid user ID'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            print(f"❌ Invalid user_id format: {user_id}")
            return Response({
                'success': False,
                'error': 'Invalid user ID format',
                'detail': 'User ID must be a number'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get all appointments for this user as patient
        appointments = Appointment.objects.filter(
            patient=user
        ).select_related('doctor', 'doctor__user').order_by('-appointment_date', '-appointment_time')
        
        print(f"✅ Found {appointments.count()} appointments for user {user.id}")
        
        appointments_data = []
        for appointment in appointments:
            # Handle case where doctor might be None
            doctor_name = "Unknown Doctor"
            doctor_specialization = ""
            doctor_experience = ""
            doctor_qualification = ""
            
            if appointment.doctor:
                # Use helper function to get doctor display name
                doctor_name = get_doctor_display_name(appointment.doctor)
                doctor_specialization = appointment.doctor.specialization or ""
                doctor_experience = appointment.doctor.experience or ""
                doctor_qualification = appointment.doctor.qualification or ""
            
            appointment_data = {
                'id': appointment.id,
                'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
                'appointment_time': appointment.appointment_time.strftime('%H:%M %p'),
                'status': appointment.status or 'scheduled',
                'duration': appointment.duration or 60,
                'symptoms': appointment.symptoms or 'Mental health consultation',
                'notes': appointment.notes or '',
                'doctor_name': doctor_name,
                'doctor_specialization': doctor_specialization,
                'doctor_experience': doctor_experience,
                'doctor_qualification': doctor_qualification,
                'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M:%S') if appointment.created_at else None,
            }
            appointments_data.append(appointment_data)
            print(f"📅 Appointment {appointment.id}: {doctor_name} - {appointment_data['status']}")
        
        return Response({
            'success': True,
            'appointments': appointments_data,
            'total_count': len(appointments_data),
            'user_name': get_user_display_name(user),  # Use helper function
            'user_id': user.id
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': str(e),
            'detail': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Simple video call session creation
class CreateVideoCallAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            appointment_id = request.data.get('appointment_id')
            user = request.user
            
            print(f"🎥 Creating video call for appointment: {appointment_id}")
            
            # Check if appointment exists and belongs to user
            appointment = Appointment.objects.get(id=appointment_id, patient=user)
            
            if appointment.status != 'confirmed':
                return Response({
                    'success': False,
                    'error': 'Only confirmed appointments can start video calls'
                }, status=400)
            
            # Simple room ID
            room_id = f"room_{appointment_id}_{user.id}"
            
            return Response({
                'success': True,
                'room_id': room_id,
                'appointment_id': appointment.id,
                'doctor_name': f"Dr. {appointment.doctor.user.get_full_name()}",
                'message': 'Video call room created successfully'
            })
            
        except Appointment.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Appointment not found'
            }, status=404)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
        






@method_decorator(csrf_exempt, name='dispatch')
class CheckDoctorAvailability(APIView):
    def get(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            
            # Simple availability check - doctor ko online consider karo
            five_minutes_ago = timezone.now() - timedelta(minutes=5)
            is_doctor_online = (
                appointment.doctor.is_online or 
                (appointment.doctor.last_seen and appointment.doctor.last_seen >= five_minutes_ago)
            )
            
            # For testing, always return online
            is_doctor_online = True
            
            return Response({
                'success': True,
                'doctor_online': is_doctor_online,
                'doctor_name': f"Dr. {appointment.doctor.user.get_full_name()}",
                'appointment_status': appointment.status
            })
            
        except Appointment.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Appointment not found'
            }, status=404)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
        








@method_decorator(csrf_exempt, name='dispatch')
class SimpleVideoCallAPI(APIView):
    def post(self, request):
        try:
            appointment_id = request.data.get('appointment_id')
            user_id = request.data.get('user_id')
            
            # Simple room creation without complex checks
            room_id = f"simple_room_{appointment_id}_{user_id}_{random.randint(1000, 9999)}"
            
            return Response({
                'success': True,
                'room_id': room_id,
                'appointment_id': appointment_id,
                'message': 'Video call room created successfully'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)



# views.py mein yeh add karen
@method_decorator(csrf_exempt, name='dispatch')
class DoctorsListAPI(APIView):
    def get(self, request):
        try:
            doctors = Doctor.objects.filter(is_verified=True).select_related('user')
            
            doctors_data = []
            for doctor in doctors:
                doctor_data = {
                    'id': doctor.id,
                    'name': f"Dr. {doctor.user.get_full_name()}",
                    'specialization': doctor.specialization,
                    'qualification': doctor.qualification,
                    'experience': f"{doctor.experience} years",
                    'hourly_rate': float(doctor.hourly_rate),
                    'is_online': doctor.is_online,
                    'rating': 4.5,  # Temporary rating
                    'languages': ['English', 'Hindi'],  # Temporary
                    'available_today': True  # Temporary
                }
                doctors_data.append(doctor_data)
            
            return Response({
                'success': True,
                'doctors': doctors_data,
                'count': len(doctors_data)
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CreateAppointmentAPI(APIView):
    def post(self, request):
        try:
            patient_id = request.data.get('patient_id')
            doctor_id = request.data.get('doctor_id')
            appointment_date = request.data.get('appointment_date')
            appointment_time = request.data.get('appointment_time')
            symptoms = request.data.get('symptoms', '')
            
            print(f"Creating appointment - Patient: {patient_id}, Doctor: {doctor_id}")
            
            # Validate required fields
            if not all([patient_id, doctor_id, appointment_date, appointment_time]):
                return Response({
                    'success': False,
                    'error': 'patient_id, doctor_id, appointment_date, and appointment_time are required'
                }, status=400)
            
            # Get patient and doctor
            from django.contrib.auth.models import User
            patient = User.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)
            
            # Create appointment
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                duration=30,  # Default 30 minutes
                status='confirmed',  # Direct confirmed for testing
                symptoms=symptoms
            )
            
            return Response({
                'success': True,
                'appointment_id': appointment.id,
                'message': 'Appointment booked successfully!',
                'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
                'appointment_time': appointment.appointment_time.strftime('%H:%M'),
                'doctor_name': f"Dr. {doctor.user.get_full_name()}"
            })
            
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Patient not found'
            }, status=404)
        except Doctor.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Doctor not found'
            }, status=404)
        except Exception as e:
            print(f"Error creating appointment: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
        








# Here we go with 
# views.py
from django.http import JsonResponse
import uuid

def get_room(request):
    return JsonResponse({
        'room_id': 'test_room',
        'ws_url': 'ws://192.168.100.212:8000/ws/video/'
    })
