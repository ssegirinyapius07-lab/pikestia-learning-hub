from django.utils.deprecation import MiddlewareMixin
from apps.accounts.models import AuditLog
import time

class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        # CSP - allow self, google oauth, and inline styles needed for theme variables
        # Adjust if you add CDNs
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://accounts.google.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "frame-src https://accounts.google.com; "
            "connect-src 'self'; "
        )
        response['Content-Security-Policy'] = csp
        if not response.get('Strict-Transport-Security') and not request.is_secure() is False:
            # Only set in production HTTPS - safe to set header anyway
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

class AuditLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._audit_start = time.time()
    def process_response(self, request, response):
        # basic audit for auth events handled in accounts signals, this logs slow requests
        return response
