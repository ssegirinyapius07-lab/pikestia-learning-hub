from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from allauth.account.signals import user_signed_up, password_changed
from .models import AuditLog

def get_ip(request):
    if not request: return None
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    AuditLog.objects.create(user=user, action='login', ip_address=get_ip(request), user_agent=request.META.get('HTTP_USER_AGENT','')[:500])

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    AuditLog.objects.create(user=user, action='logout', ip_address=get_ip(request), user_agent=request.META.get('HTTP_USER_AGENT','')[:500])

@receiver(user_login_failed)
def log_failed(sender, credentials, request, **kwargs):
    AuditLog.objects.create(action='login_failed', ip_address=get_ip(request), metadata={'email': credentials.get('email','')})

@receiver(user_signed_up)
def log_signup(sender, request, user, **kwargs):
    AuditLog.objects.create(user=user, action='signup', ip_address=get_ip(request))

@receiver(password_changed)
def log_pw_change(sender, request, user, **kwargs):
    AuditLog.objects.create(user=user, action='password_change', ip_address=get_ip(request))
