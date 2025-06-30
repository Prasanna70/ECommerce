from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('register/', views.admin_register, name='admin_register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'), 
    path('profile-setup/', views.profile_setup, name='profile_setup'),
    path('my-profile/', views.view_profile, name='view_profile'),
     # Forgot password form
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        success_url='done/' 
    ), name='forgot_password'),

    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
    template_name='registration/password_reset_confirm.html',
    success_url=reverse_lazy('adminpanel:password_reset_complete')
      ), name='password_reset_confirm'),

    # Success message after password reset
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]