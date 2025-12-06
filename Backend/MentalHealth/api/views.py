import json
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import CustomUser, ArticleLike
from django.core.exceptions import ValidationError
import re
from django.http import JsonResponse


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser  # Import your User model

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    try:
        print("Login endpoint called")
        data = request.data
        email = data.get('email')
        password = data.get('password')

        print(f"Received login attempt - Email: {email}")

        if not email or not password:
            print("Login failed: Email or password missing")
            return Response({"error": "Both email and password are required"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Find user by email
        try:
            user = CustomUser.objects.get(email=email)
            print(f"User found: {user.email}")
        except CustomUser.DoesNotExist:
            print("User not found")
            return Response({"error": "Invalid email or password"}, 
                          status=status.HTTP_401_UNAUTHORIZED)

        # Check password (using Django's password checking)
        if check_password(password, user.password):
            print("Password matched - Login successful")
            
            # Build profile image URL
            profile_image_url = None
            if user.profile_image:
                profile_image_url = request.build_absolute_uri(user.profile_image.url)
            
            # Return user data with all required fields
            return Response({
                "success": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "profile_image": profile_image_url,
                    "phone_number": user.phone_number,
                    "gender": user.gender,
                    "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
                    "weight": float(user.weight) if user.weight else None,
                    "hasCompletedProfile": user.has_completed_profile,
                    "hasCompletedAssessment": user.has_completed_assessment,
                    "role" : "doctor" if user.is_staff else "user",
                }
            }, status=status.HTTP_200_OK)
        else:
            print("Password does not match")
            return Response({"error": "Invalid email or password"}, 
                          status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response({"error": "An internal server error occurred"}, 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def signup_view(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '').strip()

        # Validation
        if not email or not password:
            return Response({"error": "Email and password are required"}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response({"error": "Invalid email format"}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        if len(password) < 8:
            return Response({"error": "Password must be at least 8 characters"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Create user with CustomUser model
        user = CustomUser.objects.create_user(
            email=email,
            username=email,  # Using email as username
            password=password,
            full_name=full_name,
            # Set default values for profile and assessment completion
            has_completed_profile=False,
            has_completed_assessment=False
        )

        return Response({
            "success": "User registered successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "hasCompletedProfile": user.has_completed_profile,
                "hasCompletedAssessment": user.has_completed_assessment,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
                "role": "doctor" if user.is_staff else "user"  # This will show "doctor" or "user"
            }
        }, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"error": str(e)}, 
                       status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An error occurred during registration"}, 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import logging
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def edit_profile(request):
    try:
        print(f"Received gender: {request.data.get('gender')}")  # Debug
        
        # Debug: Log all incoming data
        logger.info(f"Received POST data: {dict(request.data)}")
        logger.info(f"Received FILES: {dict(request.FILES)}")
        logger.info(f"Request method: {request.method}")
        
        # Get the user based on user_id (preferred) or email
        user_id = request.data.get('user_id')
        email = request.data.get('email')
        
        if not user_id and not email:
            return Response({'error': 'User ID or Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if user_id:
                user = CustomUser.objects.get(id=user_id)
            else:
                user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update user profile fields
        if 'full_name' in request.data:
            user.full_name = request.data['full_name']
            logger.info(f"Updating full_name to: {request.data['full_name']}")
        
        if 'gender' in request.data:
            gender_value = request.data['gender'].lower()
    
            # Map frontend values to database values
            gender_mapping = {
                'male': 'male',
                'female': 'female',
                'other': 'other',
                'prefer_not_to_say': 'prefer_not_to_say'
            }
    
            if gender_value in gender_mapping:
                user.gender = gender_mapping[gender_value]
                logger.info(f"Updating gender to: {user.gender}")
            else:
                logger.warning(f"Invalid gender value: {gender_value}")

        if 'date_of_birth' in request.data:
            user.date_of_birth = request.data['date_of_birth']
            logger.info(f"Updating date_of_birth to: {request.data['date_of_birth']}")
        
        if 'phone_number' in request.data:
            user.phone_number = request.data['phone_number']
            logger.info(f"Updating phone_number to: {request.data['phone_number']}")
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            logger.info(f"Received profile image: {request.FILES['profile_image'].name}")
            # Delete old profile image if exists
            if user.profile_image:
                user.profile_image.delete(save=False)
            user.profile_image = request.FILES['profile_image']
        else:
            logger.info("No profile image received")
        
        # Mark profile as completed
        user.has_completed_profile = True
        user.save()

        # Build profile image URL
        profile_image_url = None
        if user.profile_image:
            profile_image_url = request.build_absolute_uri(user.profile_image.url)
        
        return Response({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'gender': user.gender,
                'date_of_birth': user.date_of_birth,
                'phone_number': user.phone_number,
                'hasCompletedProfile': user.has_completed_profile,
                'hasCompletedAssessment': user.has_completed_assessment,
                'profile_image': profile_image_url,
                "role" : "doctor" if user.is_staff else "user"
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}", exc_info=True)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.middleware.csrf import get_token
#  Create a Django view to provide CSRF tokens
@api_view(['GET'])
def get_csrf_token(request):
    return Response({'csrfToken': get_token(request)})


@csrf_exempt
@api_view(['POST'])
def update_profile_view(request):
    try:
        data = request.data
        user_id = data.get('user_id')
        
        # Find user
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Update user profile fields
        # Add your profile fields here
        if 'full_name' in data:
            user.full_name = data['full_name']
        # Add other profile fields
        
        # Mark profile as completed
        user.has_completed_profile = True
        user.save()
        
        return Response({
            "success": "Profile updated successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "hasCompletedProfile": user.has_completed_profile,
                "hasCompletedAssessment": user.has_completed_assessment,
                "role" : "doctor" if user.is_staff else "user"
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": "An error occurred during profile update"}, 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    










from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import AudioAnalysis

User = get_user_model()

@api_view(['POST'])
def audio_analysis_view(request):
    try:
        # Get user data from request
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        if not user_id:
            return Response(
                {'success': False, 'message': 'User ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create user
        try:
            user = User.objects.get(id=user_id)
            user.has_completed_assessment = True
            user.save()



        except User.DoesNotExist:
            # Create new user if doesn't exist
            user = User.objects.create(
                id=user_id,
                username=username or f'user_{user_id}',
                email=email or f'user_{user_id}@example.com'
            )
        
        # Check if audio file is in the request
        if 'audio' not in request.FILES:
            return Response(
                {'success': False, 'message': 'No audio file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        audio_file = request.FILES['audio']
        
        # Validate file type
        allowed_types = ['audio/m4a', 'audio/mp3', 'audio/wav', 'audio/aac', 'audio/x-m4a']
        if audio_file.content_type not in allowed_types:
            return Response(
                {'success': False, 'message': 'Invalid file type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if audio_file.size > max_size:
            return Response(
                {'success': False, 'message': 'File too large (max 10MB)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create audio analysis record
        audio_analysis = AudioAnalysis.objects.create(
            user=user,
            audio_file=audio_file,
            status='uploaded'
        )
        
        # Process the audio (your analysis logic here)
        audio_analysis.status = 'completed'
        audio_analysis.analysis_result = {
            'emotion': 'neutral',
            'confidence': 0.85,
            'key_phrases': ['sample phrase 1', 'sample phrase 2'],
            'sentiment_score': 0.6
        }
        audio_analysis.save()
        
        return Response({
            'success': True,
            'message': 'Audio analysis completed successfully',
            'analysis_id': audio_analysis.id
        })
        
    except Exception as e:
        print(f"Audio analysis error: {str(e)}")
        
        # Update status if we created a record but processing failed
        if 'audio_analysis' in locals():
            audio_analysis.status = 'failed'
            audio_analysis.save()
            
        
        return Response(
            {'success': False, 'message': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    


# assessments/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Assessment
from .serializers import AssessmentSerializer

User = get_user_model()

from transformers import pipeline
import json
import logging
from django.db import transaction
import uuid
import base64
from django.core.files.base import ContentFile
from .models import UserScore

logger = logging.getLogger(__name__)

# Pretrained model load (load once) - moved here for shared access
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

@api_view(['POST'])
def create_assessment(request):
    user_id = request.data.get('user')
    
    if not user_id:
        return Response(
            {'error': 'User ID is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Create a copy of the data
    data = request.data.copy()
    data.pop('user', None)
    
    # Handle captured_image if it's base64
    captured_image_data = data.pop('captured_image', None)
    
    # Create assessment without captured_image first
    assessment = Assessment(user=user, **data)
    
    # Handle base64 image data
    if captured_image_data:
        print(f"Received image data, length: {len(captured_image_data)}")
        
        try:
            # If it's a base64 string (not data URI)
            if isinstance(captured_image_data, str) and len(captured_image_data) > 100:
                # Generate unique filename
                filename = f"expression_{uuid.uuid4().hex[:8]}.jpg"
                
                # Decode base64 string
                image_data = base64.b64decode(captured_image_data)
                
                # Create ContentFile and save to ImageField
                assessment.captured_image.save(
                    filename, 
                    ContentFile(image_data),
                    save=False
                )
                print(f"Image saved successfully as: {filename}")
                
            else:
                print("Invalid image data received")
                
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            # Continue without image if there's an error
    
    try:
        with transaction.atomic():
            # Save assessment first
            assessment.save()
            
            # Calculate and create UserScore with emotion detection
            user_score = calculate_user_score(assessment, data)
            user_score.save()
            
            serializer = AssessmentSerializer(assessment)
            
            return Response(
                {
                    'message': 'Assessment created successfully', 
                    'data': serializer.data,
                    'score_details': {
                        'total_score': user_score.total_score,
                        'breakdown': {
                            'basic_info_score': user_score.age_score + user_score.bmi_score + user_score.sleep_score,
                            'mood_score': user_score.mood_score,
                            'text_emotion_score': user_score.text_sentiment_score + user_score.text_emotion_score + user_score.text_negative_keywords_score,
                            'image_emotion_score': user_score.image_expression_score + user_score.image_fatigue_score + user_score.image_darkcircles_score + user_score.image_stressmicro_score,
                            'voice_emotion_score': user_score.voice_tone_score + user_score.voice_pitch_score + user_score.voice_speed_score + user_score.voice_hesitation_score + user_score.voice_stress_score
                        }
                    }
                }, 
                status=status.HTTP_201_CREATED
            )
    except Exception as e:
        return Response(
            {'error': f'Error creating assessment: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

def detect_text_emotion(text):
    """
    Detect emotion from text and return scores for text emotion components
    """
    if not text or not text.strip():
        return {
            "text_sentiment_score": 0,
            "text_emotion_score": 0,
            "text_negative_keywords_score": 0
        }
    
    try:
        # Process emotion detection
        result = emotion_pipeline(text)
        
        # Get primary emotion and score
        primary_emotion = result[0]['label']
        confidence = result[0]['score']
        
        # 1️⃣ Sentiment Polarity Score (10 points)
        # Negative emotions get higher scores (worse mental health)
        negative_emotions = ['anger', 'disgust', 'fear', 'sadness']
        positive_emotions = ['joy', 'surprise', 'neutral']
        
        if primary_emotion in negative_emotions:
            # Scale sentiment score based on confidence (0-10 points)
            text_sentiment_score = min(10, confidence * 10)
        elif primary_emotion in positive_emotions:
            # Positive emotions get lower scores (better mental health)
            text_sentiment_score = min(3, confidence * 3)  # Max 3 for positive
        else:
            text_sentiment_score = 5  # Neutral
        
        # 2️⃣ Emotion Category Score (10 points)
        emotion_score_map = {
            'anger': 10,      # Highest score for anger
            'disgust': 9,     # High score for disgust
            'fear': 8,        # High score for fear
            'sadness': 7,     # Medium-high for sadness
            'surprise': 4,    # Medium-low for surprise (can be positive/negative)
            'neutral': 2,     # Low for neutral
            'joy': 0,         # Zero for joy (positive emotion)
        }
        
        text_emotion_score = emotion_score_map.get(primary_emotion.lower(), 5)
        
        # 3️⃣ Negative Keywords Count Score (5 points)
        # Count negative words in text
        negative_keywords = ['sad', 'angry', 'depressed', 'anxious', 'stress', 
                           'tired', 'exhausted', 'hopeless', 'lonely', 'hurt',
                           'bad', 'terrible', 'awful', 'hate', 'cant', "can't"]
        
        text_lower = text.lower()
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        # Score based on negative word count (0-5 points)
        if negative_count >= 5:
            text_negative_score = 5
        elif negative_count >= 3:
            text_negative_score = 3
        elif negative_count >= 1:
            text_negative_score = 1
        else:
            text_negative_score = 0
        
        return {
            "text_sentiment_score": round(text_sentiment_score, 2),
            "text_emotion_score": text_emotion_score,
            "text_negative_keywords_score": text_negative_score
        }
        
    except Exception as e:
        logger.error(f"Error in emotion detection: {str(e)}")
        return {
            "text_sentiment_score": 0,
            "text_emotion_score": 0,
            "text_negative_keywords_score": 0
        }

def calculate_user_score(assessment, data):
    """
    Calculate UserScore based on assessment data with emotion detection
    """
    user_score = UserScore(user=assessment.user)
    
    # 1️⃣ Basic Info (Total 10 points)
    # Age score (2 points)
    age = data.get('age', 0)
    if age > 20:
        user_score.age_score = 2
    else:
        user_score.age_score = 1
    
    # BMI/Weight score (4 points)
    weight = data.get('weight', 0)
    if weight > 50:
        user_score.bmi_score = 2
    else:
        user_score.bmi_score = 2
    
    # Sleep score (4 points)
    sleep_quality = data.get('sleep_quality', '').lower()
    if sleep_quality == 'excellent':
        user_score.sleep_score = 4
    elif sleep_quality == 'good':
        user_score.sleep_score = 3
    elif sleep_quality == 'fair':
        user_score.sleep_score = 2
    elif sleep_quality == 'worst':
        user_score.sleep_score = 1
    else:
        user_score.sleep_score = 0
    
    # 2️⃣ Mood Sticker (Total 10 points)
    mood = data.get('mood', '').lower()
    if mood == 'happy':
        user_score.mood_score = 0
        user_score.mood_label = 'Happy'
    elif mood == 'neutral':
        user_score.mood_score = 2
        user_score.mood_label = 'Neutral'
    elif mood == 'low':
        user_score.mood_score = 5
        user_score.mood_label = 'Low'
    elif mood == 'sad':
        user_score.mood_score = 8
        user_score.mood_label = 'Sad'
    elif mood == 'angry':
        user_score.mood_score = 10
        user_score.mood_label = 'Angry'
    else:
        user_score.mood_score = 0
        user_score.mood_label = 'Unknown'
    
    # 3️⃣ Text Emotion Detection (Total 25 points)
    # Get text from assessment (assuming you have a text field)
    user_text = data.get('user_text', '') or data.get('text', '') or data.get('description', '')
    
    text_emotion_scores = detect_text_emotion(user_text)
    user_score.text_sentiment_score = text_emotion_scores['text_sentiment_score']
    user_score.text_emotion_score = text_emotion_scores['text_emotion_score']
    user_score.text_negative_keywords_score = text_emotion_scores['text_negative_keywords_score']
    
    # 4️⃣ Image Emotion Recognition (Total 25 points) - Currently set to 0
    user_score.image_expression_score = 0
    user_score.image_fatigue_score = 0
    user_score.image_darkcircles_score = 0
    user_score.image_stressmicro_score = 0
    
    # 5️⃣ Voice Emotion (Total 30 points) - Currently set to 0
    user_score.voice_tone_score = 0
    user_score.voice_pitch_score = 0
    user_score.voice_speed_score = 0
    user_score.voice_hesitation_score = 0
    user_score.voice_stress_score = 0
    
    # Calculate total score
    user_score.total_score = (
        user_score.age_score + user_score.bmi_score + user_score.sleep_score +  # Basic Info (10)
        user_score.mood_score +  # Mood (10)
        user_score.text_sentiment_score + user_score.text_emotion_score + user_score.text_negative_keywords_score +  # Text Emotion (25)
        user_score.image_expression_score + user_score.image_fatigue_score + user_score.image_darkcircles_score + user_score.image_stressmicro_score +  # Image Emotion (25)
        user_score.voice_tone_score + user_score.voice_pitch_score + user_score.voice_speed_score + user_score.voice_hesitation_score + user_score.voice_stress_score  # Voice Emotion (30)
    )
    
    return user_score



from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer

class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializer

class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer




import json
@api_view(["POST"])
def like_article(request, pk):
    try:
        # Get user ID from request body
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        if not user_id:
            return JsonResponse({
                'success': False,
                'error': 'User ID is required'
            }, status=400)
        
        # Get user and article
        user = get_object_or_404(User, id=user_id)
        article = get_object_or_404(Article, pk=pk)
        
        # Check if user already liked the article
        existing_like = ArticleLike.objects.filter(
            article=article, 
            user=user
        ).first()
        
        if existing_like:
            # Unlike the article
            existing_like.delete()
            liked = False
            message = "Article unliked successfully"
        else:
            # Like the article
            ArticleLike.objects.create(article=article, user=user)
            liked = True
            message = "Article liked successfully"
        
        # Get updated like count - direct query approach
        like_count = ArticleLike.objects.filter(article=article).count()
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': like_count,
            'message': message
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Like article error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)



@api_view(["GET"])
def check_article_like_status(request, pk):
    try:
        user_id = request.GET.get('user_id')
        
        if not user_id:
            return JsonResponse({
                'success': False,
                'error': 'User ID is required'
            }, status=400)
        
        user = get_object_or_404(User, id=user_id)
        article = get_object_or_404(Article, pk=pk)
        
        # Check if user already liked the article
        is_liked = ArticleLike.objects.filter(article=article, user=user).exists()
        like_count = ArticleLike.objects.filter(article=article).count()
        
        return JsonResponse({
            'success': True,
            'is_liked': is_liked,
            'like_count': like_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)





# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Article, ArticleView
import json
from django.utils import timezone

@csrf_exempt
@require_http_methods(["POST"])
def track_article_view(request, pk):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')  # Can be null for anonymous users
        
        article = get_object_or_404(Article, pk=pk)
        
        # Create view record
        ArticleView.objects.create(
            article=article,
            user_id=user_id  # This will be null if user_id is not provided
        )
        
        # Get updated total views from the serializer field
        total_views = article.views.count()
        
        return JsonResponse({
            'success': True,
            'total_views': total_views,
            'message': 'View tracked successfully'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
# View to get article views statistics



@require_http_methods(["GET"])
def get_article_views(request, pk):
    try:
        article = get_object_or_404(Article, pk=pk)
        
        total_views = article.views.count()
        unique_user_views = article.views.exclude(user__isnull=True).values('user').distinct().count()
        anonymous_views = article.views.filter(user__isnull=True).count()
        
        # Today's views
        today = timezone.now().date()
        todays_views = article.views.filter(viewed_at__date=today).count()
        
        return JsonResponse({
            'success': True,
            'total_views': total_views,
            'unique_user_views': unique_user_views,
            'anonymous_views': anonymous_views,
            'todays_views': todays_views
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)