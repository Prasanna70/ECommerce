from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Admin
from .forms import *
from .utils import generate_otp, send_otp_email
import random
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse_lazy

# Create your views here.
def admin_home(request):
    return render(request, 'dashboard.html')


# Temporary store for OTP registration data (replace with session or DB in production)
temp_data_store = {}

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            otp = generate_otp()
            email = form.cleaned_data['email']
            temp_data_store[email] = {
                'data': form.cleaned_data,
                'otp': otp
            }
            send_otp_email(email, otp)
            request.session['pending_email'] = email
            return redirect('adminpanel:verify_otp')
    else:
        form = AdminRegistrationForm()
    return render(request, 'register.html', {'form': form})

# # === OTP Verification View ===
def verify_otp(request):
    email = request.session.get('pending_email')
    if not email:
        return redirect('admin_register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        expected_otp = temp_data_store.get(email, {}).get('otp')

        if entered_otp == expected_otp:
            data = temp_data_store[email]['data']
            admin = Admin(
                full_name=data['full_name'],
                email=data['email'],
                mobile=data['mobile'],
                # role=data['role'],
            )
            admin.set_password(data['password'])
            admin.crn = "MCW" + str(random.randint(1000000, 9999999))
            admin.save()
            del temp_data_store[email]
            return redirect('adminpanel:admin_login')
        else:
            return HttpResponse("Invalid OTP")
    return render(request, 'verify_otp.html')

# # === Admin Login View ===
@csrf_exempt
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Session expiry based on Remember Me
            if not remember_me:
                request.session.set_expiry(0) 
            else:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days

            if not user.last_login:  # First time login
                return redirect('profile_setup')
            return redirect('adminpanel:admin_home')
        else:
            messages.error(request, "Invalid Email / CRN / Mobile or Password.")
    return render(request, 'login.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('adminpanel:login')

# def admin_login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         admin = authenticate(request, email=email, password=password)
#         if admin is not None:
#             login(request, admin)
#             if not admin.profile_completed:
#                 return redirect('adminpanel:profile_setup')
#             return redirect('adminpanel:admin_home')
#         else:
#             messages.error(request, 'Invalid credentials')
#     return render(request, 'login.html')
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("adminpanel:dashboard")  # or home
#         else:
#             messages.error(request, "Invalid credentials")
#     return render(request, "login.html")

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        if entered_otp == stored_otp:
            messages.success(request, "OTP verified successfully.")
            return redirect('adminpanel:profile_setup')
        else:
            messages.error(request, "Invalid OTP")
    return render(request, 'verify_otp.html')


# @login_required
# def admin_home(request):
#     return render(request, 'dashboard.html')

@login_required
def profile_setup(request):
    admin = request.user
    if admin.profile_completed:
        return redirect('adminpanel:admin_home')

    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES, instance=admin)
        if form.is_valid():
            form.save()
            admin.profile_completed = True
            admin.save()
            messages.success(request, 'Profile setup complete!')
            return redirect('adminpanel:admin_home')
    else:
        form = AdminProfileForm(instance=admin)
    return render(request, 'profile_setup.html', {'form': form})

@login_required
def view_profile(request):
    return render(request, 'view_profile.html', {'admin': request.user})

def admin_logout_view(request):
    logout(request)
    return redirect('adminpanel:login')


User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse('adminpanel:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            subject = "Reset your password"
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'uid': uid,
                'token': token,
                'protocol': 'http',
                'domain': request.get_host(),
                'reset_link': reset_link,
            })
            send_mail(subject, message, None, [user.email])
        return render(request, 'password_reset_done.html')  # or success message

    return render(request, 'forgot_password.html')
