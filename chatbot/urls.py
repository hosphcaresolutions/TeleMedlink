from django.urls import path
from .views import chatbot_view
from .views import ask_question
from . import views


urlpatterns = [
    path('chat/', chatbot_view, name='chatbot_view'),
    path('ask/', views.ask_question, name='ask_question'),
    path('doctors/chat/', chatbot_view, name='doctor_chat'),   
]
