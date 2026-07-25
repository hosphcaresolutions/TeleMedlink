from django.urls import path
from .views import  doctor_dashboard, profile, doctor_blogs, search_blogs, blogs_category, view_blog, post_comment, upload_blog, doctor_myblogs, view_appointments, report_view
from chatbot.views import chatbot_view, ask_question
from . import views

#app_name = 'doctors'

urlpatterns = [
  path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),
  path('profile/', profile, name='doctor_profile'),
  path('doctor_blogs/', doctor_blogs, name='doctor_blogs'),
  path('search/',search_blogs,name='search_blogs'),
  path('category/<str:cat>/',blogs_category,name='categories'),
  path('upload_blog/', upload_blog,name="upload_blog"),
  path('blog/<int:blog_id>/',view_blog,name='blog'),
  path('comment/',post_comment,name='comment'),
  path('doctor_myblogs/', doctor_myblogs,name="myblogs"),
  #path('doctor_drafts/',doctor_drafts , name='doctor_drafts'),
  path('upload_blog/<int:blog_id>/', upload_blog, name='upload_blog'),
  path('doctor_view_appointments/', view_appointments, name='view_appointments'),
  path('chat/', chatbot_view, name='chat'),
  path('ask/', ask_question, name='ask_question'),

  
  path('documents/', views.documents_view, name='doctor_documents'),
  path('documents/download/', views.download_appointments_pdf, name='doctor_documents_download'),
  
]
