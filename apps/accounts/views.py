from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from .forms import RegistrationForm, ThemeForm
from .models import User, AuditLog
from django.contrib.auth.forms import PasswordChangeForm

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # require email verification via allauth
            user.save()
            # allauth will send verification
            messages.success(request, 'Check your email to verify your account.')
            return redirect('/accounts/login/')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
@require_http_methods(["GET","POST"])
def settings_view(request):
    if request.method == 'POST':
        form = ThemeForm(request.POST, instance=request.user)
        if form.is_valid():
            u = form.save(commit=False)
            u.last_theme_sync = timezone.now()
            u.save()
            AuditLog.objects.create(user=request.user, action='theme_change', metadata={'mode': u.display_mode})
            messages.success(request, f'Theme set to {u.display_mode}')
            return redirect('account_settings')
    else:
        form = ThemeForm(instance=request.user)
    pw_form = PasswordChangeForm(request.user)
    return render(request, 'accounts/settings.html', {'theme_form': form, 'pw_form': pw_form})

@login_required
@require_http_methods(["POST"])
def update_theme_ajax(request):
    # Server-side theme persistence - for authenticated users
    mode = request.POST.get('display_mode')
    if mode in User.DisplayMode.values:
        request.user.display_mode = mode
        request.user.last_theme_sync = timezone.now()
        request.user.save(update_fields=['display_mode','last_theme_sync'])
        request.session['display_mode'] = mode
        return redirect(request.META.get('HTTP_REFERER','/'))
    return redirect('/')

@login_required
@require_http_methods(["POST"])
def change_password_view(request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password changed successfully')
    else:
        messages.error(request, 'Password change failed')
    return redirect('account_settings')
