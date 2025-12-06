from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import traceback
from .utils import chatbot_instance

@csrf_exempt
@require_http_methods(["POST"])
def chat_message(request):
    try:
        # Print request body for debugging
        print("Received request body:", request.body)
        
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        print("Received message:", message)
        
        if not message:
            return JsonResponse({
                'success': False,
                'error': 'Message is required'
            }, status=400)
        
        # Get response from chatbot
        response = chatbot_instance.generate_response(message)
        
        print("Generated response:", response)
        
        return JsonResponse({
            'success': True,
            'response': response,
            'user_message': message
        })
        
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", str(e))
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=400)
        
    except Exception as e:
        print("Internal Server Error:", str(e))
        print("Traceback:", traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'Mental Health Chatbot',
        'version': '1.0.0'
    })