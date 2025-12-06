from transformers import pipeline
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

# Pretrained model load (load once)
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

@csrf_exempt
@api_view(['POST'])
def detect_emotion(request):
    try:
        logger.info(f"Request received - Content-Type: {request.content_type}")
        
        # Get text from request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            text = data.get('text', '')
        else:
            text = request.POST.get('text', '')
        
        logger.info(f"Received text length: {len(text)} characters")
        
        if not text or not text.strip():
            logger.warning("Empty text received")
            return JsonResponse({
                "error": "No text provided",
                "status": "error"
            }, status=400)
        
        # Process emotion detection
        result = emotion_pipeline(text)
        
        # Get all emotions with scores for potential future use
        emotions = []
        for item in result:
            emotions.append({
                "label": item['label'],
                "score": float(item['score'])
            })
        
        # Return detailed response
        response_data = {
            "status": "success",
            "input_text": text,
            "primary_emotion": emotions[0]['label'],
            "confidence": emotions[0]['score'],
            "all_emotions": emotions,
            "analysis": {
                "text_length": len(text),
                "word_count": len(text.split())
            }
        }
        
        logger.info(f"Analysis complete: {emotions[0]['label']} ({emotions[0]['score']:.2f})")
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON format received")
        return JsonResponse({
            "error": "Invalid JSON format",
            "status": "error"
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({
            "error": "Internal server error",
            "details": str(e),
            "status": "error"
        }, status=500)