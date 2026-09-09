from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


# ─── Auth Forms ────────────────────────────────────────────────────────────────

class LoginForm(AuthenticationForm):
    """Custom login form using Django's built-in AuthenticationForm."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )
    error_messages = {
        'invalid_login': "Invalid username or password. Please try again.",
        'inactive': "This account is inactive.",
    }


class RegisterForm(UserCreationForm):
    """Registration form — allows student and faculty to self-register."""

    ALLOWED_ROLES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]

    first_name    = forms.CharField(max_length=100, required=True)
    last_name     = forms.CharField(max_length=100, required=True)
    email         = forms.EmailField(required=True)
    role          = forms.ChoiceField(choices=ALLOWED_ROLES, required=True)
    department    = forms.CharField(max_length=100, required=False)
    enrollment_no = forms.CharField(max_length=20, required=False,
                                    help_text="Only for students.")

    class Meta:
        model  = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'role', 'department', 'enrollment_no',
                  'password1', 'password2')

    def clean(self):
        cleaned = super().clean()
        role          = cleaned.get('role')
        enrollment_no = cleaned.get('enrollment_no')
        if role == 'student' and not enrollment_no:
            self.add_error('enrollment_no', 'Enrollment number is required for students.')
        return cleaned

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


# ─── Profile Forms ─────────────────────────────────────────────────────────────

class ProfileEditForm(forms.ModelForm):
    """Allow user to update their own profile details."""

    class Meta:
        model  = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'department', 'enrollment_no']
        widgets = {
            'first_name':    forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name':     forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email':         forms.EmailInput(attrs={'placeholder': 'email@college.edu'}),
            'phone':         forms.TextInput(attrs={'placeholder': '9876543210'}),
            'department':    forms.TextInput(attrs={'placeholder': 'BCA / B.Tech / MCA'}),
            'enrollment_no': forms.TextInput(attrs={'placeholder': 'BCA2024001'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.role != 'student':
            self.fields['enrollment_no'].widget = forms.HiddenInput()
            self.fields['enrollment_no'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs    = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already in use by another account.")
        return email


class ChangePasswordForm(forms.Form):
    """Simple password change form."""
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Current password'}),
        label="Current Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New password (min. 8 chars)'}),
        label="New Password", min_length=8
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        label="Confirm New Password"
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password1')
        p2 = cleaned.get('new_password2')
        if p1 and p2 and p1 != p2:
            self.add_error('new_password2', 'Passwords do not match.')
        return cleaned
