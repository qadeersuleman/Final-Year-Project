from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)

# --------------------------
# SYSTEM PROMPT (Improved)
# --------------------------
SYSTEM_PROMPT = """
You are a warm, simple, and compassionate mental-health therapist chatbot.
Your job is to support the user's feelings, worries, stress, emotions, or personal struggles.

Guidelines:
- Keep English very simple. No difficult words.
- Responses must be short (3–5 lines max).
- Be calm, soft, and understanding.
- Focus only on emotions, stress, anxiety, sadness, relationships, healing, comfort, or motivation.
- If user asks about random knowledge or unrelated topics, gently guide them back to how they are feeling.
- Never give medical diagnoses or instructions.
- If user expresses self-harm thoughts, respond with empathy and suggest crisis support immediately.
"""

CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die",
    "hurt myself", "can't live", "end everything"
]

def detect_crisis(text):
    t = text.lower()
    return any(word in t for word in CRISIS_KEYWORDS)


# --------------------------
# SIMPLE MEMORY (SESSION-BASED)
# --------------------------
CHAT_HISTORY = {}
MAX_HISTORY = 6   # only last 6 messages


@csrf_exempt
def mental_health_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)
    user_msg = data.get("message", "")
    session_id = data.get("session_id", "default")

    print("User message:", user_msg)
    print("Session ID:", session_id)

    # Crisis detection
    if detect_crisis(user_msg):
        reply = (
            "I am really sorry you are feeling this way. You are not alone. "
            "If you feel unsafe, please reach out to someone you trust or your local emergency number. "
            "In Pakistan, you can call Umang Helpline at 0311-7786264. "
            "Your feelings matter. I'm here with you. "
        )
        return JsonResponse({"reply": reply, "crisis": True})

    # Prepare session memory
    if session_id not in CHAT_HISTORY:
        CHAT_HISTORY[session_id] = []

    # store user message
    CHAT_HISTORY[session_id].append({"role": "user", "content": user_msg})

    # limit memory window
    if len(CHAT_HISTORY[session_id]) > MAX_HISTORY:
        CHAT_HISTORY[session_id] = CHAT_HISTORY[session_id][-MAX_HISTORY:]

    # Build prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(CHAT_HISTORY[session_id])

    try:
        response = client.chat.completions.create(
            model=settings.MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        bot_reply = response.choices[0].message.content.strip()
        print("Bot reply:", bot_reply)

        # save bot reply in history
        CHAT_HISTORY[session_id].append({"role": "assistant", "content": bot_reply})

        return JsonResponse({
            "success": True,
            "response": bot_reply,
            "user_message": user_msg
        })

    except Exception as e:
        print("Groq Error:", e)
        return JsonResponse({"error": "Something went wrong."}, status=500)
