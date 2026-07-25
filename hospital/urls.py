from django.contrib import admin
from django.conf import settings
from django.urls import path ,include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # For built-in auth views

# Django admin customization
admin.site.site_header = "TelemedLink Admin Dashboard"
admin.site.site_title = "TelemedLink Admin Dashboard"
admin.site.index_title = "Welcome to Telemedlink Admin Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('doctors/', include('doctors.urls')),
    path('patients/', include(('patients.urls', 'patients'), namespace='patients')),
    path('chatbot/', include('chatbot.urls')),
    
    # Global logout route
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),


]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
