from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm,ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from .models import Admin

# 🔹 Admin Registration Form
class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,validators=[validate_password],label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Admin
        fields = ['full_name', 'email', 'mobile','password','confirm_password']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get('password')
    #     confirm = cleaned_data.get('confirm_password')
    #     if password and confirm and password != confirm:
    #         raise forms.ValidationError("Passwords do not match")
    #     return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Admin.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if Admin.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("Mobile already exists")
        return mobile


# 🔹 Admin Login Form
class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(label="Email or CRN", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# 🔹 One-Time Profile Setup Form (First Login)
class ProfileSetupForm(forms.ModelForm):
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password",
        validators=[validate_password]
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Admin
        fields = ['full_name', 'mobile', 'profile_image']

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


# 🔹 Change Password Form (for profile settings)
class AdminChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput, validators=[validate_password])
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)


# 🔹 Optional: Profile Update Form (excluding password)
class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['full_name', 'mobile', 'address', 'role', 'profile_image']