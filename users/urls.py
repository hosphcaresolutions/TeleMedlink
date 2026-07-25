from django.urls import path
from .views import register, login_view, forgot_view, reset_view,logout_view
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views  # Add this import
from . import views # Import your custom views if you have any
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

# Add this for namespace
app_name = 'users'

urlpatterns = [

    path('', login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', register, name='register'),
    #path('password-reset/', forgot_view, name='password-reset'),
    #path('reset/<str:token>/', reset_view, name='reset'),
    path('logout/', logout_view, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    #password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html', success_url='/users/password_reset_done/'), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url='/users/reset/done/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=staticfiles_urlpatterns()