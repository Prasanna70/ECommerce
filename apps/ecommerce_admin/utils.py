# ecommerce_admin/utils.py

import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = 'Your Admin Panel OTP Verification'
    message = f'Hello,\n\nYour OTP is: {otp}\n\nUse this to verify your email.\n\nRegards,\nERP System'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)