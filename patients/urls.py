from django.urls import path
from .views import  patient_dashboard, book_appointment, my_appointments, patient_confirm_book
from doctors.views import doctor_blogs,search_blogs, profile,blogs_category, view_blog, post_comment 
from .views import patient_dashboard, faq_view
from .views import report_view
from .views import location_view
from . import views
from django.contrib.auth import views as auth_views  # For built-in logout


app_name = 'patients' # namespace for app patient.

urlpatterns = [
  path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
  path('profile/', profile, name='patient_profile'),
  path('blogs/', doctor_blogs, name='patient_blogs'),
  path('search/',search_blogs,name='search_blogs'),
  path('category/<str:cat>/',blogs_category,name='categories'),
  path('blog/<int:blog_id>/',view_blog,name='blog'),
  path('comment/',post_comment,name='comment'),
  
  path('book_appointment/', book_appointment, name='book_appointment'),
  path('my_appointments/', my_appointments, name='my_appointments'),
  path('patient_confirm_book/<str:doctor>/', patient_confirm_book, name='patient_confirm_book'),
  
  
  path('reports/', report_view, name='report'),
  path('documents/', views.documents_view, name='patient_documents'),
  path('documents/download/', views.download_appointments, name='download_appointments'),

  path('faq/', faq_view, name='faq'),
  path('location/', location_view, name='location'),

  # Add the logout route here if missing
  path('logout/', auth_views.LogoutView.as_view(next_page='patients:login'), name='logout'),
]