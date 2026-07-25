from django.shortcuts import render
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


#def chatbot_view(request):
#    return render(request, 'chatbot/patients/chat.html')
 
#@login_required
def chatbot_view(request):
    if request.user.is_authenticated and request.user.is_doctor:  # Check if user is a doctor
        return render(request, 'chatbot/doctors/chat.html')
    return render(request, 'chatbot/patients/chat.html')
    

genai.configure(api_key="AIzaSyBoqP3bsFYAESaH3TmUQdIbus2ai2Fyrlo")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="precise and concise outputs",
)

@csrf_exempt
@require_POST
def ask_question(request):
    question = request.POST.get("question")
    if not question:
        return JsonResponse({"error": "Question is required"}, status=400)

    chat_session = model.start_chat(history=[{"role": "user", "parts": [question]}])
    response = chat_session.send_message(question)

    return JsonResponse({"answer": response.text})