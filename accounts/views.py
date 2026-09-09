from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import LoginForm, RegisterForm, ProfileEditForm, ChangePasswordForm
from .decorators import login_required_custom


# ─── Auth Views ────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}! 👋")
            next_url = request.GET.get('next', 'dashboard:index')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.role          = form.cleaned_data['role']
            user.department    = form.cleaned_data.get('department', '')
            user.enrollment_no = form.cleaned_data.get('enrollment_no', '')
            user.save()
            messages.success(
                request,
                f"Account created! Welcome, {user.first_name}. Please sign in."
            )
            return redirect('accounts:login')
        else:
            messages.error(request, "Please fix the errors below.")

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    username = request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f"You've been signed out, {username}. See you soon!")
    return redirect('accounts:login')


# ─── Profile Views ─────────────────────────────────────────────────────────────

@login_required_custom
def profile_view(request):
    """View own profile + booking history summary."""
    from bookings.models import Booking
    my_bookings = Booking.objects.filter(
        requester=request.user
    ).select_related('equipment').order_by('-created_at')

    stats = {
        'total':     my_bookings.count(),
        'active':    my_bookings.filter(status='issued').count(),
        'pending':   my_bookings.filter(status='pending').count(),
        'completed': my_bookings.filter(status='completed').count(),
    }
    recent = my_bookings[:5]

    return render(request, 'accounts/profile.html', {
        'user_obj': request.user,
        'stats':    stats,
        'recent':   recent,
    })


@login_required_custom
def profile_edit(request):
    """Edit own profile details + optional password change."""
    user       = request.user
    edit_form  = ProfileEditForm(request.POST or None, instance=user)
    pwd_form   = ChangePasswordForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get('action', 'profile')

        # ── Update Profile ────────────────────────────────────────
        if action == 'profile' and edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')

        # ── Change Password ───────────────────────────────────────
        elif action == 'password' and pwd_form.is_valid():
            current_pwd = pwd_form.cleaned_data['current_password']
            new_pwd     = pwd_form.cleaned_data['new_password1']

            if not user.check_password(current_pwd):
                pwd_form.add_error('current_password', 'Incorrect current password.')
            else:
                user.set_password(new_pwd)
                user.save()
                # Keep session alive after password change
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully!")
                return redirect('accounts:profile')

    return render(request, 'accounts/profile_edit.html', {
        'edit_form': edit_form,
        'pwd_form':  pwd_form,
    })
