from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import role_required
from django.contrib.auth.models import User
from django.db import transaction

@login_required
@role_required(['Staff'])
def edit_user_view(request, user_id):
    user = User.objects.get(id=user_id)
    profile = user.profile
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST.get('email')
        profile.mobile = request.POST.get('mobile')
        profile.department = request.POST.get('department')
        profile.role = request.POST.get('role')
        user.save()
        profile.save()
        messages.success(request, f"{user.username} updated successfully.")
    return redirect('user_list')


@login_required
@role_required(['Staff'])
def delete_user_view(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if user:
        user.delete()
        messages.success(request, f"User '{user.username}' deleted.")
    return redirect('user_list')


@login_required
@role_required(['Staff'])
def reset_password_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        new_password = request.POST['password']
        user.set_password(new_password)
        user.save()
        messages.success(request, f"Password reset for '{user.username}'.")
    return redirect('user_list')

@login_required
@role_required(['Staff'])
def add_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password').strip()
        role = request.POST.get('role')
        mobile = request.POST.get('mobile', '').strip()
        department = request.POST.get('department')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('user_list')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('user_list')

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password)
                from .models import Profile
                Profile.objects.create(user=user, role=role, mobile=mobile, department=department)
                messages.success(request, f"User '{username}' added successfully.")
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")

    return redirect('user_list')

@login_required
@role_required(['Staff'])
def user_list_view(request):
    users = User.objects.all().select_related('profile').order_by('username')
    departments = ['MDO', 'Accounts', 'CRM', 'Sales']  # ✅ send to template
    return render(request, 'accounts/user_list.html', {
        'users': users,
        'departments': departments
    })


def home_redirect(request):
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            role = getattr(getattr(user, 'profile', None), 'role', None)
            if role == 'Staff':
                return redirect('staff_dashboard')
            elif role == 'Doer':
                return redirect('doer_dashboard')
            else:
                messages.error(request, 'Role not assigned.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@login_required
@role_required(['Staff'])
def staff_dashboard(request):
    return render(request, 'accounts/staff_dashboard.html')


@login_required
@role_required(['Doer'])
def doer_dashboard(request):
    return render(request, 'accounts/doer_dashboard.html')
